"""Extraction structurée de factures (PDF texte ou image) via Claude vision."""
import base64
import json
from anthropic import Anthropic

SYSTEM = """Tu extrais les données d'une facture fournisseur. Tu renvoies UNIQUEMENT du JSON strict :

{
  "supplier_name": string,
  "supplier_vat": string | null,
  "invoice_number": string,
  "invoice_date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD" | null,
  "currency": "EUR" | "USD" | ...,
  "amount_ht": number,
  "amount_vat": number,
  "amount_ttc": number,
  "line_items": [{ "description": string, "qty": number, "unit_price": number, "total": number }],
  "anomalies": string[]
}

Signale dans "anomalies" : totaux incohérents, TVA suspecte, dates bizarres, doublons."""


def extract_invoice_from_pdf_bytes(pdf_bytes: bytes, client: Anthropic) -> dict:
    b64 = base64.standard_b64encode(pdf_bytes).decode()
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": b64}},
                {"type": "text", "text": "Extrais les données de cette facture."},
            ],
        }],
    )
    try:
        return json.loads(msg.content[0].text.strip())
    except json.JSONDecodeError:
        return {"error": "parse_failed", "raw": msg.content[0].text[:1000]}


def extract_invoice_from_text(text: str, client: Anthropic) -> dict:
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        system=SYSTEM,
        messages=[{"role": "user", "content": text}],
    )
    try:
        return json.loads(msg.content[0].text.strip())
    except json.JSONDecodeError:
        return {"error": "parse_failed", "raw": msg.content[0].text[:1000]}
