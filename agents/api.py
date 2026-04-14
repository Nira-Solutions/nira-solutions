"""API HTTP unique pour Railway — dispatch vers les agents.
Déclenché par n8n ou par le dashboard."""
import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from agents.support_agent.run import process_email

app = FastAPI(title="Nira Agents API")


def check_auth(token: str | None):
    if token != f"Bearer {os.environ.get('NIRA_AGENT_TOKEN', '')}":
        raise HTTPException(401, "unauthorized")


class SupportReq(BaseModel):
    agent_id: str
    email_text: str
    gmail_thread: dict | None = None


@app.post("/v1/support/process")
def support_process(req: SupportReq, authorization: str | None = Header(None)):
    check_auth(authorization)
    try:
        return process_email(req.agent_id, req.email_text, req.gmail_thread)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/health")
def health():
    return {"ok": True}
