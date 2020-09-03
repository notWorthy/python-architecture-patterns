from datetime import date, timedelta

import pytest

from domain.model import allocate, Batch, OrderLine, OutOfStock

today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(weeks=2)

def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "RETRO-CLOCK", 100, eta=today)
    medium = Batch("normal-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    latest = Batch("slow-batch", "RETRO-CLOCK", 100, eta=later)
    line = OrderLine("oref", "RETRO-CLOCK", 10)
    allocate(line, [medium, latest, earliest])
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100 

def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    result = allocate(line, [in_stock_batch, shipment_batch])
    assert result == in_stock_batch.reference

def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])
    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])


