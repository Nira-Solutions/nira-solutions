"""Charge la configuration d'un tenant depuis Supabase.

Tous les agents passent par ici — garantit que le kill switch et les settings
par client sont respectés à chaque exécution.
"""
from dataclasses import dataclass
import os
from supabase import create_client, Client


def _sb() -> Client:
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])


@dataclass
class Tenant:
    id: str
    name: str
    slug: str
    plan: str
    tone: str
    signature: str
    paused: bool


@dataclass
class Agent:
    id: str
    tenant_id: str
    type: str
    name: str
    config: dict
    mode: str  # draft | auto | paused


class TenantPausedError(Exception):
    pass


def load_tenant(tenant_id: str) -> Tenant:
    row = _sb().table("tenants").select("*").eq("id", tenant_id).single().execute().data
    return Tenant(**{k: row[k] for k in ["id", "name", "slug", "plan", "tone", "signature", "paused"]})


def load_agent(agent_id: str) -> Agent:
    row = _sb().table("agents").select("*").eq("id", agent_id).single().execute().data
    return Agent(**{k: row[k] for k in ["id", "tenant_id", "type", "name", "config", "mode"]})


def assert_active(tenant: Tenant, agent: Agent) -> None:
    if tenant.paused or agent.mode == "paused":
        raise TenantPausedError(f"tenant={tenant.slug} agent={agent.name} est en pause")
