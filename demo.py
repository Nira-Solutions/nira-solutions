"""Démo support-agent : traite tous les emails du dossier sample_emails/
et affiche classification + réponse générée. Log en JSONL."""
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from agents.support_agent.classifier import classify
from agents.support_agent.responder import respond

SAMPLES = ROOT / "agents" / "support-agent" / "sample_emails"
LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)
LOG_FILE = LOGS / "support-agent.jsonl"


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERREUR : ANTHROPIC_API_KEY manquante dans .env")
        sys.exit(1)

    client = Anthropic()
    emails = sorted(SAMPLES.glob("*.txt"))
    print(f"\n{'='*70}\n  NIRA SUPPORT AGENT — DEMO\n  {len(emails)} emails à traiter\n{'='*70}\n")

    t0 = time.time()
    for path in emails:
        text = path.read_text(encoding="utf-8")
        t_start = time.time()
        category = classify(text, client)
        reply = respond(text, category, client)
        elapsed = time.time() - t_start

        print(f"\n── {path.name} ──")
        print(f"  Catégorie : {category.upper()}  ({elapsed:.1f}s)")
        print(f"  Réponse :\n")
        for line in reply.split("\n"):
            print(f"    {line}")

        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": datetime.now().isoformat(),
                "file": path.name,
                "category": category,
                "reply": reply,
                "latency_s": round(elapsed, 2),
            }, ensure_ascii=False) + "\n")

    total = time.time() - t0
    print(f"\n{'='*70}")
    print(f"  Traité {len(emails)} emails en {total:.1f}s  →  log : {LOG_FILE}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
