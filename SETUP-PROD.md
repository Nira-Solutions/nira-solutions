# Setup Production — Checklist

Tous les comptes sont à créer par Nicolas (sécurité = pas de délégation). Je t'accompagne à chaque étape : après chaque création, colle-moi l'URL/clé et je continue la config.

**Secrets déjà générés** : voir `.secrets-prod.local` (gitignored). Ne les régénère pas.

---

## ① Supabase (15 min)

1. https://supabase.com → Sign in → **New project**
   - Name : `nira-prod`
   - Region : **Frankfurt (eu-central-1)** — RGPD
   - DB password : utiliser 1Password, sauvegarder
2. Attendre ~2 min provisioning
3. **SQL Editor** → **New query** :
   - Coller `backend/supabase/migrations/0001_init.sql` → Run
   - Coller `backend/supabase/migrations/0002_match_knowledge_rpc.sql` → Run
4. **Settings → API** : récupérer
   - `Project URL`
   - `anon / public key`
   - `service_role key` (⚠ secret côté serveur uniquement)
5. **Authentication → Providers** : activer Email (magic link), désactiver signup public
6. Envoie-moi les 3 valeurs (URL + anon + service_role) → je prépare la suite

---

## ② Google OAuth — Gmail (10 min)

1. https://console.cloud.google.com → créer projet **Nira Solutions**
2. APIs & Services → Library → activer **Gmail API**
3. **OAuth consent screen** :
   - Type : External, In production
   - App name : Nira Solutions
   - User support email : nicolas.raes@teatower.com
   - App logo : (optionnel)
   - Homepage : https://nira-solutions.github.io/nira-solutions/
   - Privacy policy : même URL (à améliorer plus tard)
   - Authorized domains : `nira-solutions.com` (une fois domaine acheté), sinon `vercel.app`
   - Scopes : ajouter `gmail.readonly`, `gmail.send`, `gmail.modify`, `userinfo.email`
4. **Credentials → Create OAuth client ID** → Web application
   - Name : `Nira Dashboard`
   - Authorized redirect URIs : (on ajoutera après Vercel deploy)
5. Envoie-moi le `client_id` et `client_secret`

---

## ③ Vercel — frontend (10 min)

1. https://vercel.com → Sign in with GitHub
2. **New Project** → Import `Nira-Solutions/nira-solutions`
3. **Configuration** :
   - Framework : Next.js (auto-détecté)
   - Root directory : `frontend`
   - Build command : `npm run build` (défaut)
4. **Environment variables** — j'enverrai le bloc à coller une fois Supabase créé
5. Deploy
6. Une fois live, envoie-moi l'URL (style `nira-solutions.vercel.app`) → je :
   - Mets à jour la redirect URI Google OAuth
   - Mets à jour `.env` avec l'URL prod

---

## ④ Railway — agents Python (10 min)

1. https://railway.app → Sign in with GitHub
2. **New Project** → Deploy from GitHub repo → `nira-solutions`
3. **Settings → Root directory** : `/` (laisser vide)
4. **Variables** : je fournirai le bloc
5. Generate domain → envoie-moi l'URL (`.railway.app`)

---

## ⑤ Stripe (15 min)

1. https://dashboard.stripe.com → mode **Test** d'abord (on passera en Live une fois validé)
2. **Products** → créer :
   - **Nira Starter** — 500€ / mois récurrent → note le `price_id`
   - **Nira Growth** — 1 200€ / mois récurrent → note le `price_id`
   - **Nira Setup** — 500€ one-shot → note le `price_id`
3. **Developers → API keys** : note `Secret key` (sk_test_...)
4. **Developers → Webhooks** (après Vercel) :
   - Endpoint : `https://<vercel-url>/api/webhooks/stripe`
   - Events : `checkout.session.completed`, `customer.subscription.deleted`, `invoice.payment_failed`
   - Note le `signing secret` (whsec_...)
5. Envoie-moi : `sk_test_...`, les 3 price_id, `whsec_...`

---

## ⑥ Voyage AI — embeddings RAG (5 min, optionnel mais recommandé)

1. https://www.voyageai.com → Sign up
2. Free tier : 50M tokens, largement suffisant pour démarrer
3. **API keys → Create key** → envoie-moi la clé

---

## ⑦ Domaine `nira-solutions.com` (optionnel, 5 min si déjà acheté)

Si pas encore acheté : https://www.namecheap.com ou https://www.gandi.net (~10€/an)
Ensuite on configure :
- `nira-solutions.com` → brochure GitHub Pages (CNAME existant)
- `app.nira-solutions.com` → Vercel
- `agents.nira-solutions.com` → Railway
- `status.nira-solutions.com` → GitHub Pages ou Better Stack

---

## ⑧ Premier tenant Teatower

Une fois tout ①→⑤ branché :
```bash
cd nira-agents
source .env
python scripts/provision_client.py \
  --name "Teatower" --slug teatower \
  --email nicolas.raes@teatower.com \
  --plan growth \
  --agents support
```

---

## Ordre recommandé

**Session 1 (aujourd'hui) :** ① Supabase → ③ Vercel (avec env partiel) → ② Google OAuth (avec redirect URI Vercel finale) → déploiement frontend fonctionnel

**Session 2 :** ④ Railway → ⑤ Stripe → ⑥ Voyage → premier tenant Teatower

**Session 3 :** ⑦ DNS + monitoring (Sentry, Better Stack) + passage Stripe Live

---

**On commence par ① Supabase.** Va créer le projet (~15 min) et quand tu reviens, colle-moi les 3 valeurs (URL + anon + service_role) dans le chat. Je prends le relais pour injecter les migrations, générer les types TypeScript, préparer le bloc d'env Vercel.
