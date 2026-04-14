# Nira Solutions — contexte repo

Ce fichier est lu par Claude à chaque session. Reste concis.

## Projet
SaaS multi-tenant d'agents IA pour PME. Marque : **Nira Solutions**, fondateur Nicolas Raes. Venture sérieuse et prioritaire — pas un side project.

## Stack
- **Frontend** : Next.js 15 App Router + Tailwind + Supabase SSR (dans `frontend/`)
- **Backend** : Supabase PG + RLS + pgvector (dans `backend/supabase/`)
- **Agents** : Python 3.12, FastAPI sur Railway (dans `agents/`)
- **Workflows** : n8n (dans `workflows/n8n/`)
- **Billing** : Stripe

## 4 agents
- `support_agent` — emails clients (classifier + responder)
- `sales_agent` — qualification leads JSON strict
- `admin_agent` — extraction factures (vision + texte)
- `supply_agent` — prévisions ruptures + commandes

Chaque agent utilise `agents/shared/` : `tenant.py`, `audit.py`, `rag.py`, `gmail.py`, `oauth.py`, `observability.py`.

## Conventions
- Python : dossiers snake_case (`support_agent`, pas `support-agent`) pour imports
- Tests : `tests/` avec `pytest`, doivent tourner sans credentials externes
- Migrations SQL : **jamais** éditer `0001_init.sql`, toujours créer `000N_xxx.sql`
- Secrets : jamais commiter (`.env*`, `.secrets-prod.local` gitignored)
- Modèle LLM par défaut : `claude-haiku-4-5-20251001` (rapide et pas cher pour le volume)
- Embeddings : Voyage AI (`voyage-3`), pas OpenAI

## État v0.2
- 4 agents codés, API FastAPI consolidée
- Dashboard Next.js complet (login, overview, agents, drafts, runs, billing, settings)
- OAuth Gmail end-to-end avec tokens chiffrés AES-GCM
- Human-in-the-loop (drafts approve/reject)
- Kill switch global sur `tenants.paused`
- CI GitHub Actions (pytest + tsc)
- Demo mode `NEXT_PUBLIC_DEMO_MODE=1` → données factices sans Supabase
- Brochure GitHub Pages + pitch deck HTML
- Contrat service + DPA RGPD (templates, relecture juriste requise)

## Gaps restants
- Voyage embeddings à brancher (stub `agents/shared/rag.py`)
- Services cloud à créer manuellement (Supabase, Vercel, Railway, Stripe, Google OAuth) — voir `SETUP-PROD.md`
- Sentry DSN à remplir (code déjà prêt)
- Premier tenant réel à provisionner
