import { NextResponse, type NextRequest } from 'next/server';
import { supabaseServer, supabaseAdmin } from '@/lib/supabase/server';
import { encrypt } from '@/lib/crypto';

export async function GET(req: NextRequest) {
  const code = req.nextUrl.searchParams.get('code');
  if (!code) return NextResponse.redirect(new URL('/dashboard/settings?err=nocode', req.url));

  const sb = await supabaseServer();
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return NextResponse.redirect(new URL('/login', req.url));

  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code,
      client_id: process.env.GOOGLE_CLIENT_ID!,
      client_secret: process.env.GOOGLE_CLIENT_SECRET!,
      redirect_uri: process.env.GOOGLE_REDIRECT_URI!,
      grant_type: 'authorization_code',
    }),
  });
  const tok = await tokenRes.json();
  if (!tok.access_token) return NextResponse.redirect(new URL('/dashboard/settings?err=token', req.url));

  const userInfo = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
    headers: { Authorization: `Bearer ${tok.access_token}` },
  }).then((r) => r.json());

  const { data: membership } = await sb.from('tenant_members').select('tenant_id').eq('user_id', user.id).single();
  const tenantId = membership?.tenant_id;
  if (!tenantId) return NextResponse.redirect(new URL('/dashboard?err=no_tenant', req.url));

  const admin = supabaseAdmin();
  await admin.from('oauth_connections').upsert({
    tenant_id: tenantId,
    provider: 'gmail',
    account_email: userInfo.email,
    access_token_encrypted: encrypt(tok.access_token),
    refresh_token_encrypted: tok.refresh_token ? encrypt(tok.refresh_token) : null,
    expires_at: new Date(Date.now() + tok.expires_in * 1000).toISOString(),
    scopes: (tok.scope ?? '').split(' '),
  });

  return NextResponse.redirect(new URL('/dashboard/settings?ok=1', req.url));
}
