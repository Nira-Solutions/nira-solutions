"""Classifie un email client entrant dans une catégorie métier."""
from anthropic import Anthropic

CATEGORIES = ["commande", "remboursement", "info_produit", "reclamation", "autre"]

SYSTEM = f"""Tu es un classifieur d'emails client pour une entreprise.
Tu réponds UNIQUEMENT avec une des catégories suivantes, sans rien d'autre :
{', '.join(CATEGORIES)}

Règles :
- "commande" = statut, suivi, livraison, modification d'une commande
- "remboursement" = demande de retour, remboursement, produit défectueux
- "info_produit" = question sur un produit, disponibilité, composition
- "reclamation" = mécontentement, plainte, problème non résolu
- "autre" = tout le reste (partenariat, recrutement, spam...)"""


def classify(email_text: str, client: Anthropic) -> str:
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=20,
        system=SYSTEM,
        messages=[{"role": "user", "content": email_text}],
    )
    result = msg.content[0].text.strip().lower()
    return result if result in CATEGORIES else "autre"
