import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen grid place-items-center p-8">
      <div className="max-w-md text-center">
        <div className="font-display text-5xl font-semibold mb-4">Nira<span className="text-accent">.</span></div>
        <p className="text-muted mb-8">Dashboard de pilotage pour vos agents IA.</p>
        <Link href="/login" className="inline-block px-6 py-3 rounded-full bg-accent text-bg font-semibold hover:bg-accent-soft transition">
          Connexion
        </Link>
      </div>
    </main>
  );
}
