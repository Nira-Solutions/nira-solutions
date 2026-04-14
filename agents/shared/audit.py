"""Journal d'audit — chaque exécution d'agent est tracée dans la table `runs`."""
import os
import time
from contextlib import contextmanager
from supabase import create_client


def _sb():
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])


@contextmanager
def run(tenant_id: str, agent_id: str, trigger: str, input_payload: dict):
    sb = _sb()
    start = time.time()
    res = sb.table("runs").insert({
        "tenant_id": tenant_id,
        "agent_id": agent_id,
        "trigger": trigger,
        "input": input_payload,
        "status": "pending",
    }).execute()
    run_id = res.data[0]["id"]
    state = {"run_id": run_id, "output": None, "status": "pending", "category": None, "error": None, "cost": 0.0}
    try:
        yield state
        status = state.get("status") or ("draft" if state.get("output") else "error")
        sb.table("runs").update({
            "output": state.get("output"),
            "status": status,
            "category": state.get("category"),
            "latency_ms": int((time.time() - start) * 1000),
            "cost_usd": state.get("cost"),
        }).eq("id", run_id).execute()
    except Exception as e:
        sb.table("runs").update({
            "status": "error",
            "error": str(e)[:500],
            "latency_ms": int((time.time() - start) * 1000),
        }).eq("id", run_id).execute()
        raise


def create_draft(tenant_id: str, run_id: str, content: str) -> str:
    res = _sb().table("drafts").insert({
        "tenant_id": tenant_id,
        "run_id": run_id,
        "content": content,
    }).execute()
    return res.data[0]["id"]
