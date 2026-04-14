"""Sales agent — qualifie leads + met à jour CRM + crée draft de relance."""
from anthropic import Anthropic
from agents.shared.tenant import load_agent, load_tenant, assert_active
from agents.shared.audit import run as audit_run, create_draft
from agents.shared.rag import retrieve, format_context
from .qualifier import qualify


def process_lead(agent_id: str, lead_text: str, lead_metadata: dict | None = None):
    agent = load_agent(agent_id)
    tenant = load_tenant(agent.tenant_id)
    assert_active(tenant, agent)

    client = Anthropic()
    context = format_context(retrieve(tenant.id, lead_text, k=3))

    with audit_run(tenant.id, agent.id, "lead", {"lead": lead_text, "meta": lead_metadata or {}}) as state:
        result = qualify(lead_text, client, context)
        state["category"] = result.get("score", "").lower()
        state["output"] = result

        if result["next_action"] in ("call_24h", "email_relance_48h"):
            create_draft(tenant.id, state["run_id"], result["suggested_reply"])
            state["status"] = "draft"
        elif result["next_action"] == "disqualify":
            state["status"] = "sent"  # no action needed
        else:
            state["status"] = "draft"

        return result
