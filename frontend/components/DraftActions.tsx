'use client';
import { useTransition } from 'react';
import { useRouter } from 'next/navigation';

export default function DraftActions({ draftId }: { draftId: string }) {
  const [pending, start] = useTransition();
  const router = useRouter();

  async function act(action: 'approve' | 'reject') {
    const reason = action === 'reject' ? prompt('Raison du rejet (optionnel)') ?? '' : undefined;
    await fetch(`/api/drafts/${draftId}/${action}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ reason }),
    });
    start(() => router.refresh());
  }

  return (
    <div className="flex gap-2">
      <button onClick={() => act('reject')} disabled={pending}
        className="px-3 py-1.5 rounded-lg text-xs border border-line hover:border-red-400">Rejeter</button>
      <button onClick={() => act('approve')} disabled={pending}
        className="px-3 py-1.5 rounded-lg text-xs bg-accent text-bg font-semibold">Approuver & envoyer</button>
    </div>
  );
}
