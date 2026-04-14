import { supabaseServer } from '@/lib/supabase/server';
import DraftActions from '@/components/DraftActions';

export default async function DraftsPage() {
  const sb = await supabaseServer();
  const { data: drafts } = await sb
    .from('drafts')
    .select('id, content, created_at, run_id, runs:run_id(input, category)')
    .is('approved_at', null)
    .is('rejected_reason', null)
    .order('created_at', { ascending: false });

  return (
    <div>
      <header className="mb-8">
        <h1 className="font-display text-4xl font-semibold">À valider</h1>
        <p className="text-muted">Réponses générées par l'agent — à approuver avant envoi.</p>
      </header>
      {!drafts || drafts.length === 0 ? (
        <div className="p-12 text-center border border-dashed border-line rounded-2xl text-muted">
          Aucune réponse en attente. L'agent est à jour. ✨
        </div>
      ) : (
        <div className="space-y-4">
          {drafts.map((d: any) => (
            <article key={d.id} className="p-6 rounded-2xl border border-line bg-card">
              <div className="flex items-center justify-between mb-4">
                <div className="text-xs text-muted">
                  {new Date(d.created_at).toLocaleString('fr-BE')} · {d.runs?.category ?? 'autre'}
                </div>
                <DraftActions draftId={d.id} />
              </div>
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <div className="text-xs uppercase text-muted mb-2">Email reçu</div>
                  <pre className="text-sm whitespace-pre-wrap font-sans text-muted">
                    {d.runs?.input?.email ?? '—'}
                  </pre>
                </div>
                <div>
                  <div className="text-xs uppercase text-muted mb-2">Réponse proposée</div>
                  <pre className="text-sm whitespace-pre-wrap font-sans">{d.content}</pre>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
