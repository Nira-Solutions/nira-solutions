-- Seed minimal pour dev local — tenant démo "Teatower"
insert into tenants (id, name, slug, plan, tone, signature)
values ('00000000-0000-0000-0000-000000000001', 'Teatower', 'teatower', 'growth',
        'chaleureux, professionnel, belge', 'L''équipe Teatower')
on conflict (slug) do nothing;

insert into agents (tenant_id, type, name, mode, config)
values
  ('00000000-0000-0000-0000-000000000001', 'support', 'Support Email FR', 'draft',
   '{"language":"fr","escalation_email":"nicolas.raes@teatower.com"}'::jsonb),
  ('00000000-0000-0000-0000-000000000001', 'sales', 'Lead Qualifier B2B', 'draft',
   '{"min_budget_eur":500}'::jsonb)
on conflict do nothing;
