# Déploiement de la stack complète

Ordre recommandé pour passer d'un repo à un SaaS en production.

## 1. Supabase (base + auth)

1. Créer un projet sur [supabase.com](https://supabase.com/dashboard) (région Frankfurt)
2. SQL Editor → coller `backend/supabase/migrations/0001_init.sql` → Run
3. (Dev) SQL Editor → coller `backend/supabase/seed.sql` → Run
4. Settings → API : récupérer `URL`, `anon key`, `service_role key`
5. Auth → Providers : activer Email (magic link)

## 2. Vercel (frontend Next.js)

1. Pousser `frontend/` sur un repo dédié **ou** connecter le monorepo en pointant `Root directory = frontend`
2. Vercel → New Project → import repo
3. Env vars : copier `.env.example` → remplir avec les valeurs Supabase
4. Deploy. Domaine custom : `app.nira-solutions.com`

## 3. Google OAuth (Gmail)

1. [console.cloud.google.com](https://console.cloud.google.com) → créer projet "Nira"
2. APIs & Services → activer Gmail API
3. OAuth consent screen → External → renseigner (logo, privacy policy URL = brochure)
4. Credentials → OAuth client ID → Web app :
   - Authorized redirect URI : `https://app.nira-solutions.com/api/auth/gmail/callback`
5. Copier client_id / secret dans Vercel env

## 4. Railway (agents Python)

1. Créer projet Railway, connecter repo
2. Service → `Root directory = /` → Nixpacks détecte Python auto
3. Env vars :
   - `ANTHROPIC_API_KEY`
   - `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`
   - `OAUTH_ENCRYPTION_KEY` (générer : `openssl rand -hex 32`)
   - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
   - `NIRA_AGENT_TOKEN` (générer : `openssl rand -hex 24`)
4. Deploy. Domaine : `agents.nira-solutions.com`

## 5. n8n (workflows)

Option A — Railway self-host (recommandé) :
1. Nouveau service Railway → template "n8n"
2. Env : `N8N_ENCRYPTION_KEY`, `NIRA_AGENT_URL=https://agents.nira-solutions.com`, `NIRA_AGENT_TOKEN=...`
3. Importer `workflows/n8n/support-gmail.json` (Settings → Import from file)
4. Connecter les credentials Gmail OAuth du client

Option B — n8n Cloud pour démarrer (plus cher mais zéro ops).

## 6. Stripe

1. Dashboard Stripe → Products :
   - Starter — 500€/mois récurrent
   - Growth — 1 200€/mois récurrent
   - Setup fee — 500€ one-shot
2. Copier les `price_id` dans Vercel env
3. Webhooks → endpoint : `https://app.nira-solutions.com/api/webhooks/stripe`
   - Events : `checkout.session.completed`, `customer.subscription.deleted`, `invoice.payment_failed`
4. Copier `STRIPE_WEBHOOK_SECRET` dans Vercel env

## 7. DNS (domaine `nira-solutions.com`)

- `@` → Vercel (A/CNAME selon registrar) — app.nira-solutions.com
- `app` → Vercel
- `agents` → Railway
- `status` → GitHub Pages (ou Better Stack)
- `www` → redirect vers apex

## 8. Monitoring

- **Sentry** : 1 projet frontend + 1 projet agents Python → DSN dans env
- **Better Stack** / **UptimeRobot** : ping `/health` toutes les 60s, alertes Slack
- **Logtail** ou **Axiom** : log drain Railway + Vercel

## 9. Premier client

```bash
python scripts/provision_client.py \
  --name "Teatower" --slug teatower --email nicolas.raes@teatower.com --plan growth \
  --agents support sales
```
