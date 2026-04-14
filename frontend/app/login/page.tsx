'use client';
import { useState } from 'react';
import { supabaseBrowser } from '@/lib/supabase/client';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    const sb = supabaseBrowser();
    const { error } = await sb.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${location.origin}/dashboard` },
    });
    setLoading(false);
    if (!error) setSent(true);
    else alert(error.message);
  }

  return (
    <main className="min-h-screen grid place-items-center p-8">
      <div className="w-full max-w-sm">
        <div className="font-display text-4xl font-semibold mb-2">Nira<span className="text-accent">.</span></div>
        <p className="text-muted mb-8 text-sm">Connexion par lien magique.</p>
        {sent ? (
          <div className="p-4 rounded-xl border border-accent bg-accent/10 text-sm">
            Lien envoyé à <b>{email}</b>. Vérifie ta boîte mail.
          </div>
        ) : (
          <form onSubmit={onSubmit} className="space-y-3">
            <input
              type="email" required placeholder="toi@entreprise.com"
              value={email} onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-card border border-line focus:border-accent outline-none"
            />
            <button
              disabled={loading}
              className="w-full py-3 rounded-full bg-accent text-bg font-semibold disabled:opacity-50"
            >
              {loading ? 'Envoi…' : 'Recevoir le lien'}
            </button>
          </form>
        )}
      </div>
    </main>
  );
}
