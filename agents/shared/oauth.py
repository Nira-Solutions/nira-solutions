"""Chargement + refresh des tokens OAuth chiffrés depuis Supabase."""
import os
import time
import base64
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from supabase import create_client


def _sb():
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])


def _key() -> bytes:
    k = os.environ["OAUTH_ENCRYPTION_KEY"]
    if len(k) != 64:
        raise RuntimeError("OAUTH_ENCRYPTION_KEY doit faire 32 bytes hex (64 chars)")
    return bytes.fromhex(k)


def decrypt(payload_b64: str) -> str:
    raw = base64.b64decode(payload_b64)
    iv, tag, ct = raw[:12], raw[12:28], raw[28:]
    return AESGCM(_key()).decrypt(iv, ct + tag, None).decode()


def encrypt(plaintext: str) -> str:
    import os as _os
    iv = _os.urandom(12)
    ct_and_tag = AESGCM(_key()).encrypt(iv, plaintext.encode(), None)
    ct, tag = ct_and_tag[:-16], ct_and_tag[-16:]
    return base64.b64encode(iv + tag + ct).decode()


def get_gmail_token(tenant_id: str) -> str:
    sb = _sb()
    row = sb.table("oauth_connections").select("*").eq("tenant_id", tenant_id).eq("provider", "gmail").single().execute().data
    if not row:
        raise RuntimeError(f"Pas de connexion Gmail pour tenant {tenant_id}")

    expires_at = row.get("expires_at")
    if expires_at and time.time() > _to_ts(expires_at) - 60:
        return _refresh(sb, row)
    return decrypt(row["access_token_encrypted"])


def _to_ts(iso: str) -> float:
    from datetime import datetime
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


def _refresh(sb, row: dict) -> str:
    refresh = decrypt(row["refresh_token_encrypted"])
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "refresh_token": refresh,
        "grant_type": "refresh_token",
    }, timeout=15)
    r.raise_for_status()
    tok = r.json()
    new_access = tok["access_token"]
    from datetime import datetime, timezone, timedelta
    new_expiry = (datetime.now(timezone.utc) + timedelta(seconds=tok["expires_in"])).isoformat()
    sb.table("oauth_connections").update({
        "access_token_encrypted": encrypt(new_access),
        "expires_at": new_expiry,
    }).eq("id", row["id"]).execute()
    return new_access
