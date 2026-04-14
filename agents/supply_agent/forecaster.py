"""Prévision ruptures de stock basée sur historique ventes."""
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class StockAlert:
    sku: str
    current_stock: int
    avg_daily_sales: float
    days_of_stock_left: float
    reorder_recommended: bool
    reorder_quantity: int
    reason: str


def forecast_alerts(
    inventory: list[dict],
    sales_last_30d: dict[str, int],
    lead_time_days: int = 7,
    safety_days: int = 7,
) -> list[StockAlert]:
    """
    inventory : [{"sku": "TEA-001", "stock": 42, "reorder_point": 20, "reorder_qty": 100}, ...]
    sales_last_30d : {"TEA-001": 150, ...}
    """
    alerts: list[StockAlert] = []
    for item in inventory:
        sku = item["sku"]
        stock = item["stock"]
        sold = sales_last_30d.get(sku, 0)
        avg = sold / 30.0
        days_left = stock / avg if avg > 0 else 999
        needs_reorder = days_left < (lead_time_days + safety_days)
        qty = item.get("reorder_qty", max(int(avg * 30), 10)) if needs_reorder else 0
        reason = (
            f"Stock {days_left:.0f}j < lead_time {lead_time_days}j + safety {safety_days}j"
            if needs_reorder else "OK"
        )
        alerts.append(StockAlert(sku, stock, avg, days_left, needs_reorder, qty, reason))
    return alerts
