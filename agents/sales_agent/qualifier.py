"""Qualifie un lead entrant et propose une action de relance."""
import json
from anthropic import Anthropic

SYSTEM = """Tu es un SDR senior B2B. Tu analyses un lead entrant (formulaire, email ou message)
et tu renvoies UNIQUEMENT du JSON strict (pas de markdown, pas de commentaire).

Schéma :
{
  "score": "HOT" | "WARM" | "COLD",
  "reasoning": "2 phrases max expliquant le scoring",
  "intent": "acheter_court_terme" | "se_renseigner" | "comparaison" | "partenariat" | "autre",
  "next_action": "call_24h" | "email_relance_48h" | "nurture_newsletter" | "disqualify",
  "suggested_reply": "email de relance court (80-120 mots)"
}

Règles de scoring :
- HOT = budget explicite > 1000€/mois OU demande de démo OU urgence exprimée
- WARM = intérêt clair + timeline < 3 mois mais pas de budget explicite
- COLD = curiosité, comparaison, pas de timeline"""


def qualify(lead_text: str, client: Anthropic, tenant_context: str = "") -> dict:
    user_msg = f"{tenant_context}\n\nLead entrant :\n{lead_text}" if tenant_context else lead_text
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )
    try:
        return json.loads(msg.content[0].text.strip())
    except json.JSONDecodeError:
        return {
            "score": "COLD", "reasoning": "parsing_error",
            "intent": "autre", "next_action": "nurture_newsletter",
            "suggested_reply": msg.content[0].text.strip()[:500],
        }
