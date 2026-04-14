"""Génère une réponse professionnelle adaptée à la catégorie."""
import os
from anthropic import Anthropic

TEMPLATES = {
    "commande": "Rassure le client, indique que tu vérifies le statut et reviens sous 24h avec un suivi précis.",
    "remboursement": "Exprime de l'empathie, explique la procédure de retour en 3 étapes, propose un geste commercial si pertinent.",
    "info_produit": "Réponds à la question produit de façon précise. Si tu manques d'info, propose un rendez-vous téléphonique.",
    "reclamation": "Excuse-toi sincèrement, prends la main sur le dossier, propose une solution concrète (geste commercial, remplacement).",
    "autre": "Accuse réception et oriente le client vers la bonne personne/service.",
}


def respond(email_text: str, category: str, client: Anthropic) -> str:
    company = os.getenv("AGENT_COMPANY_NAME", "notre entreprise")
    tone = os.getenv("AGENT_COMPANY_TONE", "professionnel et chaleureux")
    signature = os.getenv("AGENT_SIGNATURE", f"L'équipe {company}")

    system = f"""Tu es un agent support client pour {company}. Ton ton : {tone}.
Instruction pour cette catégorie ({category}) : {TEMPLATES[category]}

Écris une réponse email courte (max 120 mots), en français, signée "{signature}".
Pas de placeholder type [NOM] ou [DATE] — reste générique si l'info manque.
Pas de salutation redondante type "Cher Monsieur/Madame" — commence directement par "Bonjour,"."""

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        system=system,
        messages=[{"role": "user", "content": f"Email reçu :\n\n{email_text}"}],
    )
    return msg.content[0].text.strip()
