from datetime import date

from model import Batch, OrderLine

today = date.today()

def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=today),
        OrderLine("order-123", sku, line_qty)
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 2)
    batch.allocate(line)

    assert batch.available_quantity == 18

def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("ELEGEANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)