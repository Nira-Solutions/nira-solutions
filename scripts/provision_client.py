"""Provision un nouveau client : crée le tenant Supabase + agents par défaut + invite owner.

Usage :
    python scripts/provision_client.py --name "Ma PME" --slug mapme --email boss@mapme.com --plan growth
"""
import argparse
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--email", required=True)
    p.add_argument("--plan", default="starter", choices=["starter", "growth", "scale"])
    p.add_argument("--agents", nargs="*", default=["support"])
    args = p.parse_args()

    sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])

    tenant = sb.table("tenants").insert({
        "name": args.name, "slug": args.slug, "plan": args.plan,
    }).execute().data[0]
    print(f"✓ Tenant créé : {tenant['id']}")

    user = sb.auth.admin.invite_user_by_email(args.email).user
    print(f"✓ Invitation envoyée à {args.email}")

    sb.table("tenant_members").insert({
        "tenant_id": tenant["id"], "user_id": user.id, "role": "owner",
    }).execute()

    for agent_type in args.agents:
        sb.table("agents").insert({
            "tenant_id": tenant["id"],
            "type": agent_type,
            "name": f"{agent_type.title()} Agent",
            "mode": "draft",
            "config": {},
        }).execute()
        print(f"✓ Agent {agent_type} créé en mode draft")

    print(f"\n✅ {args.name} est provisionné.")
    print(f"   Dashboard : https://app.nira-solutions.com/dashboard")
    print(f"   Tenant ID : {tenant['id']}")


if __name__ == "__main__":
    main()
