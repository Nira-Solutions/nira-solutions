'use client';
export default function ConnectGmailButton() {
  return (
    <a href="/api/auth/gmail/start"
      className="inline-block px-4 py-2 rounded-full bg-accent text-bg font-semibold text-sm">
      + Connecter Gmail
    </a>
  );
}
