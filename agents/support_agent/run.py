"""Support agent — version multi-tenant, branchée Supabase + Gmail + RAG.

Invocation :
    python -m agents.support_agent.run --agent-id <uuid> --email-text "..."
    python -m agents.support_agent.run --agent-id <uuid> --gmail-msg-id <id>
"""
import argparse
import os
from anthropic import Anthropic
from agents.shared.tenant import load_agent, load_tenant, assert_active
from agents.shared.audit import run as audit_run, create_draft
from agents.shared.rag import retrieve, format_context
from agents.shared.gmail import Gmail
from agents.shared.oauth import get_gmail_token
from .classifier import classify
from .responder import respond


def process_email(agent_id: str, email_text: str, gmail_thread: dict | None = None):
    agent = load_agent(agent_id)
    tenant = load_tenant(agent.tenant_id)
    assert_active(tenant, agent)

    os.environ.setdefault("AGENT_COMPANY_NAME", tenant.name)
    os.environ.setdefault("AGENT_COMPANY_TONE", tenant.tone)
    os.environ.setdefault("AGENT_SIGNATURE", tenant.signature)

    client = Anthropic()
    input_payload = {"email": email_text, "gmail_thread_id": gmail_thread.get("id") if gmail_thread else None}

    with audit_run(tenant.id, agent.id, "email", input_payload) as state:
        category = classify(email_text, client)
        state["category"] = category

        context = format_context(retrieve(tenant.id, email_text, k=4))
        prompt = f"{context}\n\n{email_text}" if context else email_text
        reply = respond(prompt, category, client)
        state["output"] = {"category": category, "reply": reply}

        if agent.mode == "draft":
            create_draft(tenant.id, state["run_id"], reply)
            state["status"] = "draft"
        elif agent.mode == "auto" and gmail_thread:
            token = get_gmail_token(tenant.id)
            Gmail(token).send_reply(
                to=gmail_thread["from"],
                subject=gmail_thread.get("subject", ""),
                body=reply,
                thread_id=gmail_thread.get("id"),
            )
            state["status"] = "sent"

        return {"category": category, "reply": reply, "status": state["status"]}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--agent-id", required=True)
    p.add_argument("--email-text", required=True)
    args = p.parse_args()
    result = process_email(args.agent_id, args.email_text)
    print(result)
