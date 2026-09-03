from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Compound:
    name: str = ""
    smiles: str = ""
    mw: float = 0.0        # g/mol
    n_protons: int = 1     # number of equivalent protons in integrated NMR signal
    area: float = 0.0      # NMR integral area


@dataclass
class InternalStandard(Compound):
    mass: float = 0.0      # mass added to sample (g)


@dataclass
class StartingMaterial(Compound):
    initial_mass: float = 0.0   # mass weighed before reaction (g)


@dataclass
class QNMRResult:
    n_is: float = 0.0               # mol
    n_sm_initial: float = 0.0       # mol
    n_sm_remaining: float = 0.0     # mol
    conversion: Optional[float] = None   # %
    products: List[dict] = field(default_factory=list)
    byproducts: List[dict] = field(default_factory=list)


class QNMRCalculator:
    """
    Calculates moles, yield, conversion, and selectivity from qNMR integrals.

    Core formula (IUPAC qNMR):
        n_X = n_IS * (A_X / A_IS) * (N_IS / N_X)
    where N = number of equivalent protons for the integrated signal.
    """

    def __init__(
        self,
        standard: InternalStandard,
        sm: StartingMaterial,
        products: List[Compound],
        byproducts: List[Compound],
    ):
        self.std = standard
        self.sm = sm
        self.products = products
        self.byproducts = byproducts

    def _n_from_area(self, n_is: float, c: Compound) -> float:
        if self.std.area <= 0 or c.n_protons <= 0 or c.area <= 0:
            return 0.0
        return n_is * (c.area / self.std.area) * (self.std.n_protons / c.n_protons)

    def calculate(self) -> QNMRResult:
        if self.std.mw <= 0:
            raise ValueError("Internal standard MW must be > 0")
        if self.std.mass <= 0:
            raise ValueError("Internal standard mass must be > 0")
        if self.std.area <= 0:
            raise ValueError("Internal standard NMR area must be > 0")

        r = QNMRResult()

        n_is = self.std.mass / self.std.mw
        r.n_is = n_is

        n_sm_rem = self._n_from_area(n_is, self.sm)
        r.n_sm_remaining = n_sm_rem

        n_sm_init: Optional[float] = None
        if self.sm.mw > 0 and self.sm.initial_mass > 0:
            n_sm_init = self.sm.initial_mass / self.sm.mw
        r.n_sm_initial = n_sm_init or 0.0

        if n_sm_init and n_sm_init > 0:
            r.conversion = max(0.0, min(100.0, (1.0 - n_sm_rem / n_sm_init) * 100.0))

        def make_entry(c: Compound) -> dict:
            n = self._n_from_area(n_is, c)
            return {
                "name": c.name,
                "smiles": c.smiles,
                "moles": n,
                "mass": n * c.mw,
                "yield": (n / n_sm_init * 100.0) if n_sm_init else None,
                "selectivity": None,
            }

        r.products = [make_entry(c) for c in self.products]
        r.byproducts = [make_entry(c) for c in self.byproducts]

        n_total = sum(e["moles"] for e in r.products + r.byproducts)
        if n_total > 0:
            for e in r.products + r.byproducts:
                e["selectivity"] = e["moles"] / n_total * 100.0

        return r
