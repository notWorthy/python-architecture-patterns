from dataclasses import dataclass
from datetime import date
from typing import Optional, Set

class OutOfStock(Exception):
    pass


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta

        self._purchased_qty = qty
        self._allocations = set() # type: Set[OrderLine]

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __lt__(self, other):
        if not self.eta:
            return True
        if not other.eta:
            return False
        return self.eta < other.eta

    def __hash__(self):
        return hash(self.reference)

    @property
    def allocated_quantity(self) -> int:
        return sum(a.qty for a in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_qty - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    def allocate(self, line: OrderLine):
        if self.can_allocate:
            self._allocations.add(line)

    def deallocate(self, line:OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

def allocate(line: OrderLine, batches: [Batch]) -> str:
    try:
        batch = next(batch for batch in sorted(batches) if batch.can_allocate(line))
    except StopIteration:
        raise(OutOfStock(f"Out of stock for sku: {line.sku}"))
    batch.allocate(line)
    return batch.reference

