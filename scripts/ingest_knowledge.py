"""Ingère une base de connaissances (FAQ, catalogue produit) dans knowledge_chunks.

Usage :
    python scripts/ingest_knowledge.py --tenant-id <uuid> --source faq --file faq.md
"""
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def chunk(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, buf = [], ""
    for p in paras:
        if len(buf) + len(p) < size:
            buf = f"{buf}\n\n{p}" if buf else p
        else:
            if buf:
                chunks.append(buf)
            buf = p
    if buf:
        chunks.append(buf)
    return chunks


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tenant-id", required=True)
    p.add_argument("--source", required=True, choices=["faq", "product_catalog", "email_history", "upload"])
    p.add_argument("--file", required=True)
    p.add_argument("--title", default=None)
    args = p.parse_args()

    sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
    text = Path(args.file).read_text(encoding="utf-8")

    doc = sb.table("knowledge_documents").insert({
        "tenant_id": args.tenant_id,
        "source": args.source,
        "title": args.title or Path(args.file).name,
        "content": text,
    }).execute().data[0]

    chunks = chunk(text)
    print(f"Document créé ({doc['id']}) — {len(chunks)} chunks")

    # TODO: générer embeddings via Voyage/OpenAI puis insert en batch
    for i, c in enumerate(chunks):
        sb.table("knowledge_chunks").insert({
            "document_id": doc["id"],
            "tenant_id": args.tenant_id,
            "content": c,
            "chunk_index": i,
            # "embedding": embed(c)  # à brancher
        }).execute()
    print(f"✓ Ingéré. ⚠ Embeddings pas encore calculés — voir agents/shared/rag.py.")


if __name__ == "__main__":
    main()
