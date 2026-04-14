import { supabaseServer } from '@/lib/supabase/server';

const PLANS = [
  { id: 'starter', name: 'Starter', price: '500€/mois', agents: 1, priceEnv: 'NEXT_PUBLIC_STRIPE_PRICE_STARTER' },
  { id: 'growth', name: 'Growth', price: '1 200€/mois', agents: 3, priceEnv: 'NEXT_PUBLIC_STRIPE_PRICE_GROWTH', featured: true },
  { id: 'scale', name: 'Scale', price: 'Sur mesure', agents: '∞' },
];

export default async function BillingPage() {
  const sb = await supabaseServer();
  const { data: tenant } = await sb.from('tenants').select('*').limit(1).single();

  return (
    <div>
      <h1 className="font-display text-4xl font-semibold mb-2">Facturation</h1>
      <p className="text-muted mb-8">Plan actuel : <b className="text-ink">{tenant?.plan ?? '—'}</b></p>
      <div className="grid grid-cols-3 gap-4">
        {PLANS.map((p) => (
          <div key={p.id} className={`p-6 rounded-2xl border ${p.featured ? 'border-accent' : 'border-line'} bg-card`}>
            <div className="font-display text-xl font-semibold">{p.name}</div>
            <div className="font-display text-3xl text-accent my-2">{p.price}</div>
            <div className="text-sm text-muted mb-6">{p.agents} agent{p.agents !== 1 ? 's' : ''}</div>
            <form action="/api/billing/checkout" method="post">
              <input type="hidden" name="plan" value={p.id} />
              <button className="w-full py-2 rounded-full bg-accent text-bg font-semibold">
                {tenant?.plan === p.id ? 'Plan actif' : 'Choisir'}
              </button>
            </form>
          </div>
        ))}
      </div>
    </div>
  );
}
