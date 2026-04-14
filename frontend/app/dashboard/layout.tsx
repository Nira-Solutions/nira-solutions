import Link from 'next/link';
import { supabaseServer } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';
import { LayoutDashboard, Bot, Inbox, Settings, CreditCard, LogOut } from 'lucide-react';

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const sb = await supabaseServer();
  const { data: { user } } = await sb.auth.getUser();
  if (!user) redirect('/login');

  const { data: tenants } = await sb.from('tenants').select('id, name, slug, paused, plan').limit(1);
  const tenant = tenants?.[0];

  const nav = [
    { href: '/dashboard', label: 'Overview', icon: LayoutDashboard },
    { href: '/dashboard/agents', label: 'Agents', icon: Bot },
    { href: '/dashboard/drafts', label: 'À valider', icon: Inbox },
    { href: '/dashboard/runs', label: 'Historique', icon: Inbox },
    { href: '/dashboard/billing', label: 'Facturation', icon: CreditCard },
    { href: '/dashboard/settings', label: 'Paramètres', icon: Settings },
  ];

  return (
    <div className="min-h-screen grid grid-cols-[260px_1fr]">
      <aside className="border-r border-line bg-bg-2 p-6 flex flex-col">
        <div className="font-display text-2xl font-semibold mb-8">Nira<span className="text-accent">.</span></div>
        <div className="text-xs text-muted mb-1">Espace</div>
        <div className="font-medium mb-6 flex items-center gap-2">
          {tenant?.name ?? '—'}
          {tenant?.paused && <span className="text-[10px] px-2 py-0.5 rounded-full bg-red-500/20 text-red-400">PAUSE</span>}
        </div>
        <nav className="space-y-1 flex-1">
          {nav.map((n) => (
            <Link key={n.href} href={n.href}
              className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm hover:bg-card transition">
              <n.icon size={16} /> {n.label}
            </Link>
          ))}
        </nav>
        <form action="/api/auth/signout" method="post">
          <button className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-muted hover:text-ink w-full">
            <LogOut size={16} /> Déconnexion
          </button>
        </form>
      </aside>
      <main className="p-8 max-w-6xl">{children}</main>
    </div>
  );
}
