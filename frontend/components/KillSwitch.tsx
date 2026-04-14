'use client';
import { useTransition } from 'react';
import { supabaseBrowser } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';

export default function KillSwitch({ tenantId, paused }: { tenantId?: string; paused?: boolean }) {
  const [pending, start] = useTransition();
  const router = useRouter();
  if (!tenantId) return null;

  async function toggle() {
    const sb = supabaseBrowser();
    await sb.from('tenants').update({ paused: !paused }).eq('id', tenantId);
    start(() => router.refresh());
  }

  return (
    <button
      onClick={toggle}
      disabled={pending}
      className={`px-4 py-2 rounded-full text-sm font-semibold transition ${
        paused ? 'bg-accent text-bg' : 'bg-red-500/20 text-red-400 hover:bg-red-500/30'
      }`}
    >
      {paused ? '▶ Réactiver les agents' : '⏸ Mettre en pause'}
    </button>
  );
}
