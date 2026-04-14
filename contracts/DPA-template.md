# Accord de Traitement des Données (DPA) — Nira Solutions

> **⚠ Template à faire relire par un juriste RGPD.** Annexe au contrat de service.
> Conforme à l'article 28 RGPD.

---

**Entre :**

**[Client]** — Responsable du traitement (« le Responsable »)
**Nira Solutions** — Sous-traitant (« le Sous-traitant »)

## 1. Objet et durée du traitement

Le Sous-traitant traite les données personnelles pour le compte du Responsable dans le cadre de la fourniture d'agents IA d'automatisation. Durée : celle du contrat de service principal.

## 2. Nature et finalité des traitements

- Lecture, classification et génération de réponses à des emails entrants
- Qualification et relance de contacts commerciaux
- Lecture et encodage de documents (factures, bons de commande)
- Gestion de stocks et commandes fournisseurs

## 3. Catégories de personnes concernées

- Clients et prospects du Responsable
- Fournisseurs et partenaires du Responsable
- Salariés et collaborateurs du Responsable (pour emails/CRM)

## 4. Catégories de données

- Données d'identification (nom, prénom, email, téléphone)
- Contenu de correspondance (emails entrants et sortants)
- Données transactionnelles (commandes, factures)
- Pas de données sensibles au sens de l'art. 9 RGPD, sauf accord exprès écrit

## 5. Obligations du Sous-traitant

- Traiter les données **uniquement sur instruction écrite** du Responsable
- Garantir la **confidentialité** (personnel formé, obligations de secret)
- Mettre en œuvre des **mesures de sécurité** (art. 32 RGPD) :
  - Chiffrement at-rest (AES-256) des tokens OAuth
  - Chiffrement in-transit (TLS 1.2+)
  - Isolation multi-tenant par Row-Level Security
  - Authentification à 2 facteurs sur accès admin
  - Logs d'audit conservés 24 mois
- **Notifier toute violation** dans les 48h (art. 33)
- Assister le Responsable pour les **droits des personnes** (accès, effacement, portabilité)
- **Supprimer ou restituer** les données en fin de contrat (choix du Responsable)

## 6. Sous-traitants ultérieurs autorisés

Le Responsable autorise les sous-traitants suivants :

| Sous-traitant | Finalité | Localisation |
|---|---|---|
| Supabase (Fly.io) | Base de données, auth | UE (Francfort) |
| Railway | Hébergement agents | US (transfert hors UE — clauses contractuelles types) |
| Anthropic | LLM Claude | US (transfert hors UE — DPA Anthropic + CCT) |
| Stripe | Paiement | IE/US |
| Vercel | Hébergement frontend | US (transfert hors UE — CCT) |

Tout changement de sous-traitant fera l'objet d'une notification préalable de 30 jours.

## 7. Transferts hors UE

Les transferts vers les États-Unis sont encadrés par les **Clauses Contractuelles Types** de la Commission européenne (décision 2021/914) et, le cas échéant, l'adhésion des sous-traitants au Data Privacy Framework.

## 8. Durée de conservation

- Contenu d'emails traités : **90 jours** par défaut (configurable)
- Logs d'audit : **24 mois**
- Base de connaissances (RAG) : durée du contrat + 30 jours

## 9. Audit

Le Responsable peut, avec un préavis de 30 jours et une fois par an, auditer la conformité du Sous-traitant (ou mandater un tiers indépendant).

## 10. Fin du traitement

À l'issue du contrat :
- Export des données sous format standard (JSON/CSV) dans les 30 jours
- Suppression définitive (y compris sauvegardes) sous 60 jours
- Certificat de destruction fourni sur demande

---

**Pour le Responsable**            **Pour le Sous-traitant**
[Nom / Fonction]                   Nicolas Raes, Nira Solutions
Date :                             Date :
