import { NextResponse, type NextRequest } from 'next/server';
import { supabaseServer } from '@/lib/supabase/server';

export async function POST(_req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const sb = await supabaseServer();
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return NextResponse.json({ error: 'unauthorized' }, { status: 401 });

  const { data: draft } = await sb.from('drafts').select('*, runs:run_id(*)').eq('id', id).single();
  if (!draft) return NextResponse.json({ error: 'not_found' }, { status: 404 });

  await sb.from('drafts').update({ approved_by: user.id, approved_at: new Date().toISOString() }).eq('id', id);
  await sb.from('runs').update({ status: 'approved' }).eq('id', draft.run_id);

  // TODO: déclencher l'envoi réel via n8n webhook ou Gmail API directement
  // await fetch(process.env.N8N_SEND_WEBHOOK!, { method: 'POST', body: JSON.stringify({ draft_id: id }) });

  return NextResponse.json({ ok: true });
}
