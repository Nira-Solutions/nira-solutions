"""Supply agent — détecte ruptures, propose commandes fournisseurs."""
from agents.shared.tenant import load_agent, load_tenant, assert_active
from agents.shared.audit import run as audit_run, create_draft
from .forecaster import forecast_alerts


def check_stock(agent_id: str, inventory: list[dict], sales_last_30d: dict[str, int]):
    agent = load_agent(agent_id)
    tenant = load_tenant(agent.tenant_id)
    assert_active(tenant, agent)

    with audit_run(tenant.id, agent.id, "cron", {"items": len(inventory)}) as state:
        alerts = forecast_alerts(inventory, sales_last_30d)
        to_order = [a for a in alerts if a.reorder_recommended]
        state["output"] = {
            "alerts_total": len(alerts),
            "to_reorder": len(to_order),
            "items": [{"sku": a.sku, "qty": a.reorder_quantity, "reason": a.reason} for a in to_order],
        }
        state["category"] = f"{len(to_order)}_reorders"
        if to_order:
            lines = "\n".join(f"• {a.sku} — {a.reorder_quantity} unités ({a.reason})" for a in to_order)
            summary = f"Commandes fournisseurs suggérées ({len(to_order)}) :\n\n{lines}"
            create_draft(tenant.id, state["run_id"], summary)
            state["status"] = "draft"
        else:
            state["status"] = "sent"
        return state["output"]
