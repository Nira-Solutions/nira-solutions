"""Vérifie que encrypt/decrypt du toolkit Python est symétrique et produit
des ciphertexts différents à chaque appel (IV random)."""
import os
import pytest

os.environ.setdefault("OAUTH_ENCRYPTION_KEY", "0" * 64)

from agents.shared.oauth import encrypt, decrypt


def test_roundtrip():
    plain = "ya29.a0ARrdaM-fake-gmail-token-example"
    ct = encrypt(plain)
    assert ct != plain
    assert decrypt(ct) == plain


def test_different_iv_each_call():
    ct1 = encrypt("same")
    ct2 = encrypt("same")
    assert ct1 != ct2  # IV random → ciphertext différent


def test_tamper_detection():
    ct = encrypt("secret")
    tampered = ct[:-4] + "AAAA"
    with pytest.raises(Exception):
        decrypt(tampered)
