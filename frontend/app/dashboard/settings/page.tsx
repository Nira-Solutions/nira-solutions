import { supabaseServer } from '@/lib/supabase/server';
import ConnectGmailButton from '@/components/ConnectGmailButton';

export default async function SettingsPage() {
  const sb = await supabaseServer();
  const { data: tenant } = await sb.from('tenants').select('*').limit(1).single();
  const { data: oauths } = await sb.from('oauth_connections').select('provider, account_email, created_at');

  return (
    <div className="max-w-2xl">
      <h1 className="font-display text-4xl font-semibold mb-8">Paramètres</h1>

      <section className="mb-10">
        <h2 className="font-display text-2xl mb-3">Identité de marque</h2>
        <form action="/api/settings/brand" method="post" className="space-y-3">
          <label className="block">
            <span className="text-xs text-muted">Ton</span>
            <input name="tone" defaultValue={tenant?.tone}
              className="w-full mt-1 px-3 py-2 rounded-lg bg-card border border-line" />
          </label>
          <label className="block">
            <span className="text-xs text-muted">Signature</span>
            <input name="signature" defaultValue={tenant?.signature}
              className="w-full mt-1 px-3 py-2 rounded-lg bg-card border border-line" />
          </label>
          <button className="px-4 py-2 rounded-full bg-accent text-bg font-semibold">Enregistrer</button>
        </form>
      </section>

      <section>
        <h2 className="font-display text-2xl mb-3">Connexions</h2>
        <div className="space-y-2 mb-4">
          {oauths?.map((o) => (
            <div key={o.provider} className="p-3 rounded-lg border border-line bg-card flex justify-between">
              <span className="capitalize">{o.provider} — {o.account_email}</span>
              <span className="text-xs text-muted">connecté</span>
            </div>
          )) ?? <div className="text-muted text-sm">Aucune connexion active.</div>}
        </div>
        <ConnectGmailButton />
      </section>
    </div>
  );
}
