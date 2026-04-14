-- Nira Solutions — schéma multi-tenant
-- Exécuter dans Supabase SQL Editor ou via `supabase db push`

create extension if not exists "vector";
create extension if not exists "pgcrypto";

-- =========================================================================
-- TENANTS & USERS
-- =========================================================================
create table if not exists tenants (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text unique not null,
  plan text not null default 'starter' check (plan in ('starter','growth','scale')),
  stripe_customer_id text,
  stripe_subscription_id text,
  tone text default 'professionnel et chaleureux',
  signature text default 'L''équipe',
  paused boolean not null default false,
  created_at timestamptz default now()
);

create table if not exists tenant_members (
  tenant_id uuid references tenants(id) on delete cascade,
  user_id uuid references auth.users(id) on delete cascade,
  role text not null default 'owner' check (role in ('owner','admin','viewer')),
  created_at timestamptz default now(),
  primary key (tenant_id, user_id)
);

-- =========================================================================
-- AGENTS (instances déployées par tenant)
-- =========================================================================
create table if not exists agents (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid not null references tenants(id) on delete cascade,
  type text not null check (type in ('support','sales','admin','supply')),
  name text not null,
  config jsonb not null default '{}'::jsonb,
  mode text not null default 'draft' check (mode in ('draft','auto','paused')),
  created_at timestamptz default now(),
  unique (tenant_id, type, name)
);

-- =========================================================================
-- OAUTH CONNECTIONS (Gmail, Outlook, etc.)
-- =========================================================================
create table if not exists oauth_connections (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid not null references tenants(id) on delete cascade,
  provider text not null check (provider in ('gmail','outlook','odoo','shopify','hubspot')),
  account_email text,
  access_token_encrypted text not null,
  refresh_token_encrypted text,
  expires_at timestamptz,
  scopes text[],
  created_at timestamptz default now(),
  unique (tenant_id, provider, account_email)
);

-- =========================================================================
-- RUNS (historique d'exécution de chaque agent) — audit log
-- =========================================================================
create table if not exists runs (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid not null references tenants(id) on delete cascade,
  agent_id uuid not null references agents(id) on delete cascade,
  trigger text not null, -- 'email', 'cron', 'manual'
  input jsonb,
  output jsonb,
  status text not null default 'pending' check (status in ('pending','draft','sent','approved','rejected','error')),
  category text,
  latency_ms int,
  cost_usd numeric(10,6),
  error text,
  created_at timestamptz default now()
);
create index if not exists runs_tenant_created_idx on runs(tenant_id, created_at desc);
create index if not exists runs_status_idx on runs(status) where status in ('draft','pending');

-- =========================================================================
-- DRAFTS (human-in-the-loop — réponses à valider)
-- =========================================================================
create table if not exists drafts (
  id uuid primary key default gen_random_uuid(),
  run_id uuid not null references runs(id) on delete cascade,
  tenant_id uuid not null references tenants(id) on delete cascade,
  content text not null,
  approved_by uuid references auth.users(id),
  approved_at timestamptz,
  rejected_reason text,
  created_at timestamptz default now()
);

-- =========================================================================
-- KNOWLEDGE BASE (RAG — FAQ, docs, historique emails)
-- =========================================================================
create table if not exists knowledge_documents (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid not null references tenants(id) on delete cascade,
  source text not null, -- 'faq', 'product_catalog', 'email_history', 'upload'
  title text,
  content text not null,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists knowledge_chunks (
  id uuid primary key default gen_random_uuid(),
  document_id uuid not null references knowledge_documents(id) on delete cascade,
  tenant_id uuid not null references tenants(id) on delete cascade,
  content text not null,
  embedding vector(1536),
  chunk_index int not null
);
create index if not exists knowledge_chunks_embedding_idx
  on knowledge_chunks using ivfflat (embedding vector_cosine_ops) with (lists = 100);
create index if not exists knowledge_chunks_tenant_idx on knowledge_chunks(tenant_id);

-- =========================================================================
-- USAGE METRICS (pour billing & rapports)
-- =========================================================================
create table if not exists usage_daily (
  tenant_id uuid not null references tenants(id) on delete cascade,
  day date not null,
  agent_type text not null,
  runs_count int not null default 0,
  cost_usd numeric(10,4) not null default 0,
  time_saved_minutes int not null default 0,
  primary key (tenant_id, day, agent_type)
);

-- =========================================================================
-- ROW LEVEL SECURITY — isolation stricte par tenant
-- =========================================================================
alter table tenants enable row level security;
alter table tenant_members enable row level security;
alter table agents enable row level security;
alter table oauth_connections enable row level security;
alter table runs enable row level security;
alter table drafts enable row level security;
alter table knowledge_documents enable row level security;
alter table knowledge_chunks enable row level security;
alter table usage_daily enable row level security;

-- Helper : renvoie les tenants auxquels l'user a accès
create or replace function current_user_tenants() returns setof uuid language sql stable as $$
  select tenant_id from tenant_members where user_id = auth.uid()
$$;

create policy "members_see_own_tenants" on tenants for select
  using (id in (select current_user_tenants()));

create policy "members_see_own_memberships" on tenant_members for select
  using (user_id = auth.uid() or tenant_id in (select current_user_tenants()));

-- Pattern répétable sur toutes les tables "scoped by tenant_id"
do $$
declare t text;
begin
  for t in select unnest(array['agents','oauth_connections','runs','drafts','knowledge_documents','knowledge_chunks','usage_daily']) loop
    execute format(
      'create policy "tenant_isolation_select" on %I for select using (tenant_id in (select current_user_tenants()))', t
    );
    execute format(
      'create policy "tenant_isolation_insert" on %I for insert with check (tenant_id in (select current_user_tenants()))', t
    );
    execute format(
      'create policy "tenant_isolation_update" on %I for update using (tenant_id in (select current_user_tenants()))', t
    );
  end loop;
end $$;
