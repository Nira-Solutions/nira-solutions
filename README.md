# Nira Agents

Agents IA pour PME — déployés clé en main.

## Agents disponibles

- **support-agent** — classifie et répond aux emails clients (MVP)
- admin-agent *(à venir)*
- sales-agent *(à venir)*
- supply-agent *(à venir)*

## Quick start — Démo support-agent

```bash
cd nira-agents
pip install -r requirements.txt
cp .env.example .env
# éditer .env et ajouter ANTHROPIC_API_KEY

python demo.py
```

Le script va :
1. Lire les emails dans `agents/support-agent/sample_emails/`
2. Classifier chacun (commande / remboursement / info / autre)
3. Générer une réponse professionnelle
4. Logger le tout dans `logs/support-agent.jsonl`

## Architecture cible

```
Client → Dashboard Next.js → Supabase → Agents Railway → n8n → Gmail/ERP/CRM
```

## Structure

```
nira-agents/
├── agents/
│   └── support-agent/
│       ├── main.py
│       ├── classifier.py
│       ├── responder.py
│       └── sample_emails/
├── workflows/n8n/          # workflows à importer dans n8n
├── frontend/               # dashboard Next.js (à venir)
├── backend/                # Supabase schema (à venir)
└── demo.py
```
