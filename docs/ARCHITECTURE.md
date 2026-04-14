# Architecture Nira Solutions

## Vue d'ensemble

```
                    ┌─────────────────────┐
                    │   Client (navigateur)│
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Frontend Next.js   │  Vercel
                    │  (dashboard + auth) │
                    └──────────┬──────────┘
                               │  (Supabase client SDK)
                    ┌──────────▼──────────┐
                    │   Supabase (PG)     │
                    │  • auth             │
                    │  • schéma tenant    │
                    │  • RLS isolation    │
                    │  • pgvector (RAG)   │
                    └──┬───────────────┬──┘
                       │               │
            ┌──────────▼───┐      ┌────▼──────────┐
            │ Agents Python│      │  n8n workflows│  Railway
            │  (Railway)   │◄─────┤  (triggers)   │
            └──────┬───────┘      └───────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
     Gmail     Odoo/Shopify  Claude API
     (OAuth)   (API)         (LLM)
```

## Composants

### Frontend (`frontend/`)
- **Next.js 15 App Router** + TypeScript + Tailwind
- **Supabase Auth** (email magic link + Google OAuth)
- Pages : login, dashboard, agents, runs, drafts (human-in-the-loop), settings, billing
- Déployé sur **Vercel**, 1 projet par env (dev/staging/prod)

### Backend (`backend/supabase/`)
- **Supabase Postgres** avec :
  - Auth intégrée
  - Row Level Security → isolation stricte par `tenant_id`
  - `pgvector` pour RAG
  - Edge Functions pour webhooks (Stripe, Gmail push notifications)
- **Tables clés** : `tenants`, `agents`, `oauth_connections`, `runs`, `drafts`, `knowledge_chunks`, `usage_daily`

### Agents (`agents/`)
- **Python 3.11+**, chaque agent = package isolé
- Shared toolkit (`agents/shared/`) : tenant loader, audit logger, RAG retriever, Gmail/Odoo clients
- Déployés sur **Railway** (1 service par type d'agent, scalable horizontalement)
- Triggers : webhook depuis n8n ou polling Supabase

### Workflows (`workflows/n8n/`)
- **n8n self-hosted** sur Railway
- Templates JSON importables (ex. `support-gmail.json` : Gmail trigger → HTTP agent → drafts)
- 1 instance n8n par tenant OU n8n partagé avec credentials scopés par tenant (selon plan)

## Flow type — support-agent (end-to-end)

1. Client Gmail reçoit un email
2. **n8n** (Gmail trigger) détecte le nouveau mail → POST vers agent Railway
3. **support-agent** (Python) :
   - Charge config tenant depuis Supabase (`tenants`, `agents`, `knowledge_chunks`)
   - Classifie (Claude Haiku)
   - Génère réponse avec RAG sur FAQ/catalogue
   - Écrit dans `runs` (status=draft) + `drafts`
4. **Dashboard Next.js** affiche le draft avec bouton Approuver / Rejeter
5. Sur approbation → n8n envoie via Gmail API → `runs.status = sent`

## Sécurité

- **Secrets tokens OAuth** : chiffrés at-rest (AES via `pgp_sym_encrypt` avec clé master hors DB)
- **RLS** : chaque requête Supabase filtre par `tenant_id` de l'user connecté
- **Kill switch** : `tenants.paused = true` → tous les agents stoppent lecture/envoi immédiatement
- **Logs d'audit** : table `runs` = source de vérité, rétention 24 mois

## Environnements

| Env | Frontend | Supabase | Agents | Usage |
|-----|----------|----------|--------|-------|
| dev | localhost:3000 | local Docker | local Python | dev |
| staging | staging.nira-solutions.com | projet staging | Railway staging | tests internes |
| prod | app.nira-solutions.com | projet prod | Railway prod | clients |

## Observabilité

- **Sentry** : erreurs frontend + agents Python
- **Logtail / Axiom** : logs applicatifs
- **Supabase logs** : requêtes DB, auth events
- **Status page** : status.nira-solutions.com (UptimeRobot ou Better Stack)

## Billing

- **Stripe** : 3 produits (Starter, Growth, Scale) + setup fee one-shot
- Webhook `/api/webhooks/stripe` → met à jour `tenants.stripe_subscription_id` + `plan`
- Downgrade/cancel → `tenants.paused = true` + email
