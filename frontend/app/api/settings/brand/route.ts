import { NextResponse, type NextRequest } from 'next/server';
import { supabaseServer } from '@/lib/supabase/server';

export async function POST(req: NextRequest) {
  const sb = await supabaseServer();
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return NextResponse.redirect(new URL('/login', req.url));
  const form = await req.formData();
  const { data: tenant } = await sb.from('tenants').select('id').limit(1).single();
  if (tenant) {
    await sb.from('tenants').update({
      tone: String(form.get('tone') ?? ''),
      signature: String(form.get('signature') ?? ''),
    }).eq('id', tenant.id);
  }
  return NextResponse.redirect(new URL('/dashboard/settings?ok=1', req.url));
}
