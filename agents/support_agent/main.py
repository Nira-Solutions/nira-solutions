"""Support agent — point d'entrée.

Usage :
    from agents.support_agent.main import handle_email
    result = handle_email("Bonjour, où en est ma commande ?")
"""
from anthropic import Anthropic
from .classifier import classify
from .responder import respond


def handle_email(email_text: str, client: Anthropic | None = None) -> dict:
    client = client or Anthropic()
    category = classify(email_text, client)
    reply = respond(email_text, category, client)
    return {
        "category": category,
        "reply": reply,
        "email_in": email_text,
    }
