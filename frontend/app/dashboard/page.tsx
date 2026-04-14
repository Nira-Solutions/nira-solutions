import { supabaseServer } from '@/lib/supabase/server';
import KillSwitch from '@/components/KillSwitch';

export default async function Overview() {
  const sb = await supabaseServer();
  const { data: tenant } = await sb.from('tenants').select('*').limit(1).single();
  const { data: agents } = await sb.from('agents').select('*').eq('tenant_id', tenant?.id ?? '');
  const { data: runsToday } = await sb
    .from('runs')
    .select('id, status, category, latency_ms, created_at')
    .gte('created_at', new Date(Date.now() - 86400000).toISOString())
    .order('created_at', { ascending: false })
    .limit(20);

  const counts = {
    total: runsToday?.length ?? 0,
    sent: runsToday?.filter((r) => r.status === 'sent').length ?? 0,
    drafts: runsToday?.filter((r) => r.status === 'draft').length ?? 0,
    errors: runsToday?.filter((r) => r.status === 'error').length ?? 0,
  };
  const savingsEur = counts.sent * 2.5;

  return (
    <div className="space-y-8">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-4xl font-semibold">Overview</h1>
          <p className="text-muted">Activité des dernières 24h</p>
        </div>
        <KillSwitch tenantId={tenant?.id} paused={tenant?.paused} />
      </header>

      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Tâches 24h', value: counts.total },
          { label: 'Envoyées', value: counts.sent },
          { label: 'À valider', value: counts.drafts },
          { label: 'Économies estimées', value: `${savingsEur}€` },
        ].map((k) => (
          <div key={k.label} className="p-5 rounded-2xl border border-line bg-card">
            <div className="text-xs text-muted mb-1">{k.label}</div>
            <div className="font-display text-3xl font-semibold text-accent">{k.value}</div>
          </div>
        ))}
      </div>

      <section>
        <h2 className="font-display text-2xl font-semibold mb-4">Agents déployés</h2>
        <div className="grid grid-cols-2 gap-4">
          {agents?.map((a) => (
            <div key={a.id} className="p-5 rounded-2xl border border-line bg-card">
              <div className="flex justify-between items-start">
                <div>
                  <div className="font-medium">{a.name}</div>
                  <div className="text-xs text-muted uppercase tracking-wider">{a.type}</div>
                </div>
                <span className={`text-[10px] px-2 py-1 rounded-full ${a.mode === 'auto' ? 'bg-accent text-bg' : 'bg-line'}`}>
                  {a.mode}
                </span>
              </div>
            </div>
          )) ?? <div className="text-muted text-sm">Aucun agent déployé.</div>}
        </div>
      </section>

      <section>
        <h2 className="font-display text-2xl font-semibold mb-4">Dernières exécutions</h2>
        <div className="rounded-2xl border border-line overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-bg-2 text-muted text-left text-xs uppercase">
              <tr>
                <th className="p-3">Heure</th>
                <th className="p-3">Catégorie</th>
                <th className="p-3">Statut</th>
                <th className="p-3 text-right">Latence</th>
              </tr>
            </thead>
            <tbody>
              {runsToday?.map((r) => (
                <tr key={r.id} className="border-t border-line">
                  <td className="p-3 text-muted">{new Date(r.created_at).toLocaleTimeString('fr-BE')}</td>
                  <td className="p-3">{r.category ?? '—'}</td>
                  <td className="p-3"><StatusBadge s={r.status} /></td>
                  <td className="p-3 text-right text-muted">{r.latency_ms ? `${r.latency_ms}ms` : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function StatusBadge({ s }: { s: string }) {
  const colors: Record<string, string> = {
    sent: 'bg-accent/20 text-accent',
    draft: 'bg-yellow-500/20 text-yellow-400',
    error: 'bg-red-500/20 text-red-400',
    pending: 'bg-line text-muted',
  };
  return <span className={`text-[10px] px-2 py-1 rounded-full ${colors[s] ?? 'bg-line'}`}>{s}</span>;
}
