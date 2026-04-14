# Nira Solutions

SaaS d'agents IA pour PME. Déploiement clé en main en 7 jours.

**🌐 Brochure :** https://nira-solutions.github.io/nira-solutions/
**📖 Architecture :** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
**🚀 Déploiement stack complète :** [docs/DEPLOY-STACK.md](docs/DEPLOY-STACK.md)
**🤝 Onboarding client :** [docs/ONBOARDING.md](docs/ONBOARDING.md)

## Structure

```
nira-agents/
├── frontend/                   # Dashboard Next.js 15 (Vercel)
│   ├── app/                    # App Router : login, dashboard, agents, drafts, billing, settings
│   ├── app/api/                # OAuth Gmail, Stripe webhooks, drafts approve/reject
│   ├── lib/                    # Supabase client, chiffrement AES-GCM
│   └── components/             # KillSwitch, DraftActions, ConnectGmail
│
├── backend/supabase/
│   ├── migrations/0001_init.sql  # schéma multi-tenant + RLS + pgvector
│   └── seed.sql                  # dev seed (Teatower)
│
├── agents/                     # Agents Python (Railway)
│   ├── shared/                 # tenant loader, audit, RAG, Gmail, OAuth
│   ├── support_agent/          # MVP : classifier + responder + run.py
│   └── api.py                  # FastAPI endpoint pour n8n
│
├── workflows/n8n/              # templates workflows importables
├── scripts/                    # provision_client.py, ingest_knowledge.py
├── contracts/                  # contrat-service + DPA RGPD (templates)
└── docs/                       # brochure HTML + guides déploiement
```

## Démarrage local rapide

```bash
# 1. Schéma DB
# → coller backend/supabase/migrations/0001_init.sql dans Supabase SQL Editor

# 2. Agents Python
cd nira-agents
pip install -r requirements.txt
cp .env.example .env
# remplir ANTHROPIC_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OAUTH_ENCRYPTION_KEY

# 3. Dashboard
cd frontend
npm install
cp .env.example .env.local
# remplir les vars Supabase + Google OAuth + Stripe
npm run dev
# → http://localhost:3000
```

## État d'avancement

### ✅ Fait (v0.1)
- Brochure commerciale (GitHub Pages)
- Schéma DB multi-tenant + RLS + pgvector
- Dashboard Next.js : auth, agents, drafts, kill switch, billing
- OAuth Gmail end-to-end (connect + token refresh chiffré)
- Support-agent Python branché Supabase (audit, drafts)
- API FastAPI pour n8n
- Template n8n Gmail → Agent
- Script provisioning client
- Contrat + DPA templates
- Status page

### 🟠 À compléter avant 1er client prod
- [ ] Brancher embeddings (Voyage AI) dans `agents/shared/rag.py`
- [ ] Créer la RPC Supabase `match_knowledge` (cosine similarity)
- [ ] Page `/dashboard/settings` : update mode agent (select non encore connecté)
- [ ] Sentry DSN intégré (frontend + agents)
- [ ] Tests E2E Playwright (login, approve draft)
- [ ] Rate limiting sur `/api/auth/gmail/start`

### 🟡 Tier 3 (après clients 1-3)
- [ ] Sales-agent, admin-agent, supply-agent
- [ ] Provisioning auto Railway + Vercel
- [ ] Doppler/Infisical pour secrets
- [ ] Page status live (Better Stack)
