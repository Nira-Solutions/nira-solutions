import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

const ALG = 'aes-256-gcm';

function key(): Buffer {
  const k = process.env.OAUTH_ENCRYPTION_KEY;
  if (!k || k.length !== 64) throw new Error('OAUTH_ENCRYPTION_KEY must be 32 bytes hex (64 chars)');
  return Buffer.from(k, 'hex');
}

export function encrypt(plaintext: string): string {
  const iv = randomBytes(12);
  const c = createCipheriv(ALG, key(), iv);
  const ct = Buffer.concat([c.update(plaintext, 'utf8'), c.final()]);
  const tag = c.getAuthTag();
  return Buffer.concat([iv, tag, ct]).toString('base64');
}

export function decrypt(payload: string): string {
  const buf = Buffer.from(payload, 'base64');
  const iv = buf.subarray(0, 12);
  const tag = buf.subarray(12, 28);
  const ct = buf.subarray(28);
  const d = createDecipheriv(ALG, key(), iv);
  d.setAuthTag(tag);
  return Buffer.concat([d.update(ct), d.final()]).toString('utf8');
}
