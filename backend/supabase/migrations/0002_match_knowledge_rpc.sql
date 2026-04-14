-- RPC utilisée par agents/shared/rag.py pour retrouver les chunks pertinents
-- Cosine similarity via pgvector. Scopée par tenant (sécurité).

create or replace function match_knowledge(
  tenant uuid,
  query_embedding vector(1536),
  match_count int default 5
)
returns table (
  id uuid,
  content text,
  document_id uuid,
  similarity float
)
language sql stable as $$
  select
    kc.id,
    kc.content,
    kc.document_id,
    1 - (kc.embedding <=> query_embedding) as similarity
  from knowledge_chunks kc
  where kc.tenant_id = tenant
    and kc.embedding is not null
  order by kc.embedding <=> query_embedding
  limit match_count;
$$;
