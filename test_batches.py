from datetime import date

from model import Batch, OrderLine

today = date.today()

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=today)
    line = OrderLine('order-ref', "SMALL-TABLE", 2)
    batch.allocate(line)

    assert batch.available_quantity == 18