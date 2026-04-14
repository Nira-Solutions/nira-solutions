import { NextResponse, type NextRequest } from 'next/server';
import Stripe from 'stripe';
import { supabaseAdmin } from '@/lib/supabase/server';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: NextRequest) {
  const sig = req.headers.get('stripe-signature')!;
  const body = await req.text();
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 400 });
  }

  const sb = supabaseAdmin();

  if (event.type === 'checkout.session.completed') {
    const s = event.data.object as Stripe.Checkout.Session;
    const tenantId = s.metadata?.tenant_id;
    if (tenantId) {
      await sb.from('tenants').update({
        plan: s.metadata?.plan,
        stripe_customer_id: s.customer as string,
        stripe_subscription_id: s.subscription as string,
        paused: false,
      }).eq('id', tenantId);
    }
  }

  if (event.type === 'customer.subscription.deleted') {
    const sub = event.data.object as Stripe.Subscription;
    await sb.from('tenants').update({ paused: true }).eq('stripe_subscription_id', sub.id);
  }

  return NextResponse.json({ received: true });
}
