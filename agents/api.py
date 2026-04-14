"""API HTTP unique pour Railway — dispatch vers les 4 agents."""
import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from agents.shared.observability import init_sentry
from agents.support_agent.run import process_email
from agents.sales_agent.run import process_lead
from agents.admin_agent.run import process_invoice
from agents.supply_agent.run import check_stock

init_sentry("agents-api")
app = FastAPI(title="Nira Agents API", version="0.2.0")


def check_auth(token: str | None):
    if token != f"Bearer {os.environ.get('NIRA_AGENT_TOKEN', '')}":
        raise HTTPException(401, "unauthorized")


class SupportReq(BaseModel):
    agent_id: str
    email_text: str
    gmail_thread: dict | None = None


class SalesReq(BaseModel):
    agent_id: str
    lead_text: str
    lead_metadata: dict | None = None


class AdminReq(BaseModel):
    agent_id: str
    text: str | None = None
    pdf_base64: str | None = None


class SupplyReq(BaseModel):
    agent_id: str
    inventory: list[dict]
    sales_last_30d: dict[str, int]


@app.post("/v1/support/process")
def support_process(req: SupportReq, authorization: str | None = Header(None)):
    check_auth(authorization)
    try:
        return process_email(req.agent_id, req.email_text, req.gmail_thread)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/v1/sales/qualify")
def sales_qualify(req: SalesReq, authorization: str | None = Header(None)):
    check_auth(authorization)
    try:
        return process_lead(req.agent_id, req.lead_text, req.lead_metadata)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/v1/admin/invoice")
def admin_invoice(req: AdminReq, authorization: str | None = Header(None)):
    check_auth(authorization)
    import base64
    try:
        pdf_bytes = base64.b64decode(req.pdf_base64) if req.pdf_base64 else None
        return process_invoice(req.agent_id, pdf_bytes=pdf_bytes, text=req.text)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/v1/supply/check")
def supply_check(req: SupplyReq, authorization: str | None = Header(None)):
    check_auth(authorization)
    try:
        return check_stock(req.agent_id, req.inventory, req.sales_last_30d)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/health")
def health():
    return {"ok": True, "version": "0.2.0", "agents": ["support", "sales", "admin", "supply"]}
