"""Récupération de contexte depuis la knowledge base du tenant (pgvector)."""
import os
from anthropic import Anthropic

# Embeddings : on passe par l'API Voyage ou OpenAI. Placeholder minimal ici —
# Anthropic n'expose pas encore d'API embeddings dédiée.
# Pour prod : utiliser voyage-3 ou text-embedding-3-small.


def embed(text: str) -> list[float]:
    # TODO: brancher Voyage AI ou OpenAI ici
    # from voyageai import Client; return Client().embed([text], model="voyage-3").embeddings[0]
    raise NotImplementedError("Brancher Voyage AI ou OpenAI pour les embeddings")


def retrieve(tenant_id: str, query: str, k: int = 5) -> list[dict]:
    """Renvoie les k chunks les plus similaires depuis knowledge_chunks."""
    import os
    from supabase import create_client
    sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
    try:
        vec = embed(query)
    except NotImplementedError:
        return []  # dégradation gracieuse tant que embeddings pas branchés
    res = sb.rpc("match_knowledge", {"tenant": tenant_id, "query_embedding": vec, "match_count": k}).execute()
    return res.data or []


def format_context(chunks: list[dict]) -> str:
    if not chunks:
        return ""
    lines = ["=== CONTEXTE DE L'ENTREPRISE ==="]
    for c in chunks:
        lines.append(f"- {c.get('content', '')[:400]}")
    lines.append("=== FIN CONTEXTE ===\n")
    return "\n".join(lines)
