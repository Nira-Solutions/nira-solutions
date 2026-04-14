import { NextResponse, type NextRequest } from 'next/server';
import { supabaseServer } from '@/lib/supabase/server';

export async function POST(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const { reason } = await req.json().catch(() => ({ reason: '' }));
  const sb = await supabaseServer();
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return NextResponse.json({ error: 'unauthorized' }, { status: 401 });

  await sb.from('drafts').update({ rejected_reason: reason || 'non spécifié' }).eq('id', id);
  const { data: draft } = await sb.from('drafts').select('run_id').eq('id', id).single();
  if (draft) await sb.from('runs').update({ status: 'rejected' }).eq('id', draft.run_id);

  return NextResponse.json({ ok: true });
}
