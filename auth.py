import sqlite3
import hashlib
import hmac
import os
from pathlib import Path

DB_PATH = Path(__file__).with_name("depthive.db")

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                organization TEXT NOT NULL,
                requested_role TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def _hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return salt.hex() + ":" + digest.hex()

def _verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, digest_hex = stored.split(":", 1)
        candidate = hashlib.scrypt(password.encode("utf-8"), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
        return hmac.compare_digest(candidate.hex(), digest_hex)
    except (ValueError, TypeError):
        return False

def create_user(name: str, email: str, organization: str, role: str, password: str):
    try:
        with _connect() as conn:
            conn.execute(
                "INSERT INTO users (full_name, email, organization, requested_role, password_hash) VALUES (?, ?, ?, ?, ?)",
                (name, email, organization, role, _hash_password(password))
            )
        return True, "Account created. You can now sign in."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

def verify_user(email: str, password: str):
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, full_name, email, organization, requested_role, password_hash FROM users WHERE email = ?",
            (email,)
        ).fetchone()
    if row and _verify_password(password, row["password_hash"]):
        return {
            "id": row["id"],
            "name": row["full_name"],
            "email": row["email"],
            "organization": row["organization"],
            "role": row["requested_role"],
        }
    return None
