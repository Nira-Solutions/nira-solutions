"""Admin agent — extraction facture → draft d'encodage."""
from anthropic import Anthropic
from agents.shared.tenant import load_agent, load_tenant, assert_active
from agents.shared.audit import run as audit_run, create_draft
from .invoice_extractor import extract_invoice_from_pdf_bytes, extract_invoice_from_text


def process_invoice(agent_id: str, *, pdf_bytes: bytes | None = None, text: str | None = None):
    agent = load_agent(agent_id)
    tenant = load_tenant(agent.tenant_id)
    assert_active(tenant, agent)

    if not pdf_bytes and not text:
        raise ValueError("pdf_bytes ou text requis")

    client = Anthropic()
    with audit_run(tenant.id, agent.id, "invoice", {"source": "pdf" if pdf_bytes else "text"}) as state:
        data = extract_invoice_from_pdf_bytes(pdf_bytes, client) if pdf_bytes else extract_invoice_from_text(text, client)
        state["output"] = data
        state["category"] = "invoice_extracted" if "error" not in data else "parse_error"
        summary = f"Facture {data.get('invoice_number', '?')} — {data.get('supplier_name', '?')} — {data.get('amount_ttc', '?')} {data.get('currency', '')}"
        create_draft(tenant.id, state["run_id"], summary)
        state["status"] = "draft"
        return data
