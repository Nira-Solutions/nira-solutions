"""Tests du moteur de prévision supply-agent — pas d'IO, exécutable sans credentials."""
from agents.supply_agent.forecaster import forecast_alerts


def test_no_reorder_when_stock_ample():
    inv = [{"sku": "A", "stock": 1000, "reorder_qty": 100}]
    sales = {"A": 30}  # 1/jour
    [a] = forecast_alerts(inv, sales, lead_time_days=7, safety_days=7)
    assert not a.reorder_recommended
    assert a.days_of_stock_left > 14


def test_reorder_when_below_threshold():
    inv = [{"sku": "B", "stock": 10, "reorder_qty": 200}]
    sales = {"B": 90}  # 3/jour → 3.3j de stock
    [a] = forecast_alerts(inv, sales, lead_time_days=7, safety_days=7)
    assert a.reorder_recommended
    assert a.reorder_quantity == 200


def test_no_sales_gives_infinite_runway():
    inv = [{"sku": "C", "stock": 5}]
    sales = {}
    [a] = forecast_alerts(inv, sales)
    assert not a.reorder_recommended


def test_multiple_items_mixed_state():
    inv = [
        {"sku": "X", "stock": 500, "reorder_qty": 100},
        {"sku": "Y", "stock": 2, "reorder_qty": 50},
    ]
    sales = {"X": 30, "Y": 60}
    alerts = forecast_alerts(inv, sales)
    by_sku = {a.sku: a for a in alerts}
    assert not by_sku["X"].reorder_recommended
    assert by_sku["Y"].reorder_recommended
