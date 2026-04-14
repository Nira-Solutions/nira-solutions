import { NextResponse, type NextRequest } from 'next/server';
import Stripe from 'stripe';
import { supabaseServer } from '@/lib/supabase/server';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

const PRICE_BY_PLAN: Record<string, string | undefined> = {
  starter: process.env.NEXT_PUBLIC_STRIPE_PRICE_STARTER,
  growth: process.env.NEXT_PUBLIC_STRIPE_PRICE_GROWTH,
};

export async function POST(req: NextRequest) {
  const form = await req.formData();
  const plan = String(form.get('plan'));
  const priceId = PRICE_BY_PLAN[plan];
  if (!priceId) return NextResponse.redirect(new URL('/dashboard/billing?err=plan', req.url));

  const sb = await supabaseServer();
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return NextResponse.redirect(new URL('/login', req.url));
  const { data: tenant } = await sb.from('tenants').select('*').limit(1).single();

  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    line_items: [{ price: priceId, quantity: 1 }],
    customer_email: user.email,
    client_reference_id: tenant?.id,
    success_url: `${req.nextUrl.origin}/dashboard/billing?ok=1`,
    cancel_url: `${req.nextUrl.origin}/dashboard/billing?cancel=1`,
    metadata: { tenant_id: tenant?.id ?? '', plan },
  });
  return NextResponse.redirect(session.url!, 303);
}
