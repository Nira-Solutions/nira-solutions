import { supabaseServer } from '@/lib/supabase/server';

export default async function AgentsPage() {
  const sb = await supabaseServer();
  const { data: agents } = await sb.from('agents').select('*');

  return (
    <div>
      <h1 className="font-display text-4xl font-semibold mb-2">Agents</h1>
      <p className="text-muted mb-8">Tes agents déployés et leur mode de fonctionnement.</p>
      <div className="grid grid-cols-2 gap-4">
        {agents?.map((a) => (
          <div key={a.id} className="p-6 rounded-2xl border border-line bg-card">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="font-medium text-lg">{a.name}</div>
                <div className="text-xs text-muted uppercase">{a.type}</div>
              </div>
              <select defaultValue={a.mode} className="bg-bg-2 border border-line rounded-lg px-3 py-1 text-sm">
                <option value="draft">Draft (humain valide)</option>
                <option value="auto">Auto (envoi direct)</option>
                <option value="paused">En pause</option>
              </select>
            </div>
            <pre className="text-xs text-muted bg-bg-2 p-3 rounded-lg overflow-x-auto">
              {JSON.stringify(a.config, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
}
