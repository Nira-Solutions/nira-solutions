# Onboarding client Nira — Checklist J0 → J7

## Avant le kick-off (J-3)

- [ ] Contrat signé (`contracts/contrat-service.md`)
- [ ] DPA signé (`contracts/DPA-template.md`)
- [ ] Paiement setup reçu (500€)
- [ ] Client a désigné un référent interne (1 personne, décisionnaire)

## J0 — Kick-off (60 min)

- [ ] Présentation du dashboard + mode "draft" (humain valide tout au démarrage)
- [ ] Identification du cas d'usage prioritaire (1 seul agent à la fois)
- [ ] Collecte des accès :
  - [ ] Compte Google Workspace (admin) → pour délégation Gmail
  - [ ] Ton de marque : 3 exemples d'emails "bien tapés" que le client a déjà envoyés
  - [ ] FAQ existante (PDF, Notion, Google Doc)
  - [ ] Catalogue produit (CSV ou API)
  - [ ] Historique 3 mois d'emails clients (export Gmail/Outlook) — optionnel mais puissant pour RAG

## J1-J2 — Provisioning

- [ ] `python scripts/provision_client.py --name "X" --slug x --email boss@x.com --plan growth`
- [ ] Le référent reçoit l'email Supabase, se connecte au dashboard
- [ ] Connexion Gmail via Settings (OAuth)
- [ ] Upload FAQ + catalogue via `scripts/ingest_knowledge.py`
- [ ] Agent configuré en mode `draft`

## J3-J5 — Calibration

- [ ] Agent traite 20-30 vrais emails en mode draft
- [ ] Référent valide/corrige → on ajuste le prompt système + knowledge base
- [ ] Taux d'approbation visé : >80% avant passage en `auto`

## J6 — Validation

- [ ] Review des 50 dernières drafts avec le référent
- [ ] Décision go/no-go mode `auto`
- [ ] Si go : activation du mode auto sur plage horaire limitée d'abord (ex. 9h-17h)

## J7 — Go-live

- [ ] Mode `auto` activé
- [ ] Monitoring actif (alertes Slack/email si latence > 10s ou taux d'erreur > 5%)
- [ ] 1er paiement mensuel prélevé (Stripe)
- [ ] Point à J+30 planifié

## Post go-live (hebdo → mensuel)

- Semaine 1 : check quotidien, corrections rapides
- Semaines 2-4 : review hebdo (30 min)
- Mois 2+ : review mensuelle + rapport automatique par email
