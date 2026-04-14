"""Wrapper Gmail API basique — lit et envoie des emails avec un token OAuth déchiffré."""
import base64
import requests
from email.message import EmailMessage


class Gmail:
    def __init__(self, access_token: str):
        self.token = access_token
        self.h = {"Authorization": f"Bearer {access_token}"}

    def list_unread(self, max_results: int = 10) -> list[dict]:
        r = requests.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            params={"q": "is:unread in:inbox", "maxResults": max_results},
            headers=self.h, timeout=15,
        )
        r.raise_for_status()
        return r.json().get("messages", [])

    def get_message(self, msg_id: str) -> dict:
        r = requests.get(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
            params={"format": "full"}, headers=self.h, timeout=15,
        )
        r.raise_for_status()
        return r.json()

    def send_reply(self, to: str, subject: str, body: str, thread_id: str | None = None) -> str:
        msg = EmailMessage()
        msg["To"] = to
        msg["Subject"] = subject if subject.lower().startswith("re:") else f"Re: {subject}"
        msg.set_content(body)
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        payload = {"raw": raw}
        if thread_id:
            payload["threadId"] = thread_id
        r = requests.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            json=payload, headers=self.h, timeout=15,
        )
        r.raise_for_status()
        return r.json()["id"]

    def mark_read(self, msg_id: str) -> None:
        requests.post(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}/modify",
            json={"removeLabelIds": ["UNREAD"]}, headers=self.h, timeout=15,
        ).raise_for_status()
