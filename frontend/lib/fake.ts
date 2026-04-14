/**
 * Demo mode : données factices pour présenter le dashboard sans Supabase.
 * Activé via NEXT_PUBLIC_DEMO_MODE=1.
 */
export const DEMO = process.env.NEXT_PUBLIC_DEMO_MODE === '1';

export const fakeTenant = {
  id: 'demo-tenant',
  name: 'Teatower (démo)',
  slug: 'teatower-demo',
  plan: 'growth',
  tone: 'chaleureux, professionnel, belge',
  signature: 'L\'équipe Teatower',
  paused: false,
};

export const fakeAgents = [
  { id: 'a1', tenant_id: 'demo-tenant', type: 'support', name: 'Support Email FR', mode: 'draft',
    config: { language: 'fr', escalation_email: 'nicolas.raes@teatower.com' } },
  { id: 'a2', tenant_id: 'demo-tenant', type: 'sales', name: 'Lead Qualifier B2B', mode: 'draft',
    config: { min_budget_eur: 500 } },
  { id: 'a3', tenant_id: 'demo-tenant', type: 'admin', name: 'Facturation auto', mode: 'auto',
    config: { odoo_journal: 'FAC' } },
];

export const fakeRuns = Array.from({ length: 18 }, (_, i) => {
  const cats = ['commande', 'remboursement', 'info_produit', 'autre', 'reclamation', 'HOT', 'WARM'];
  const statuses = ['sent', 'sent', 'sent', 'draft', 'draft', 'sent', 'error'];
  return {
    id: `r${i}`,
    category: cats[i % cats.length],
    status: statuses[i % statuses.length],
    latency_ms: 1200 + Math.floor(Math.random() * 3000),
    created_at: new Date(Date.now() - i * 37 * 60 * 1000).toISOString(),
  };
});

export const fakeDrafts = [
  {
    id: 'd1', created_at: new Date(Date.now() - 1000 * 60 * 7).toISOString(),
    run_id: 'r3',
    content:
      "Bonjour Sophie,\n\nMerci pour votre message. Votre commande #4821 a bien été expédiée hier soir via bpost. Le numéro de suivi (BE00123...) vient d'être ajouté à votre espace client — livraison prévue vendredi, largement à temps pour le week-end.\n\nSi quoi que ce soit, on reste à votre disposition.\n\nBelle journée,\nL'équipe Teatower",
    runs: {
      category: 'commande',
      input: {
        email:
          "Objet : Ma commande #4821\n\nBonjour, j'ai passé commande lundi et je n'ai toujours pas reçu de numéro de suivi. J'en ai besoin pour le week-end. Merci, Sophie",
      },
    },
  },
  {
    id: 'd2', created_at: new Date(Date.now() - 1000 * 60 * 23).toISOString(),
    run_id: 'r5',
    content:
      "Bonjour Marc,\n\nJe suis vraiment désolée pour cette boîte abîmée — ce n'est pas digne de ce qu'on essaie de faire chez nous. Je vous renvoie gratuitement un Rouge Printanier dès demain (pas besoin de nous renvoyer la boîte abîmée). Vous devriez la recevoir sous 48h.\n\nEncore toutes mes excuses,\nL'équipe Teatower",
    runs: {
      category: 'remboursement',
      input: {
        email:
          'Bonjour, boîte de Rouge Printanier arrivée écrasée, infusettes abîmées. Remboursement ou remplacement ?',
      },
    },
  },
];
