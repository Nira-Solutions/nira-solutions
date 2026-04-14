import { supabaseServer } from '@/lib/supabase/server';
import { DEMO, fakeRuns } from '@/lib/fake';

export default async function RunsPage() {
  let runs: any[] = [];
  if (DEMO) {
    runs = fakeRuns;
  } else {
    const sb = await supabaseServer();
    const { data } = await sb.from('runs').select('*').order('created_at', { ascending: false }).limit(100);
    runs = data ?? [];
  }

  return (
    <div>
      <h1 className="font-display text-4xl font-semibold mb-2">Historique d'exécutions</h1>
      <p className="text-muted mb-8">100 dernières actions des agents — audit complet.</p>
      <div className="rounded-2xl border border-line overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-bg-2 text-muted text-left text-xs uppercase">
            <tr>
              <th className="p-3">Date</th>
              <th className="p-3">Catégorie</th>
              <th className="p-3">Statut</th>
              <th className="p-3 text-right">Latence</th>
            </tr>
          </thead>
          <tbody>
            {runs.map((r) => (
              <tr key={r.id} className="border-t border-line hover:bg-bg-2">
                <td className="p-3 text-muted">{new Date(r.created_at).toLocaleString('fr-BE')}</td>
                <td className="p-3">{r.category ?? '—'}</td>
                <td className="p-3">{r.status}</td>
                <td className="p-3 text-right text-muted">{r.latency_ms ? `${r.latency_ms}ms` : '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
