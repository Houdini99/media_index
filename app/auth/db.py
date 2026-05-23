"""All raw SQL for the auth domain.

Grouped here so that route handlers in routes.py never embed SQL.
Schema and migrations preserved exactly as they were in the original auth.py.
"""
import sqlite3
from datetime import datetime

from ..config import Config


def _conn():
    return sqlite3.connect(Config.AUTH_DB)


def init_auth_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            enc_key BLOB
        );
    """)
    cur.execute("PRAGMA table_info(users)")
    cols = [c[1] for c in cur.fetchall()]
    if 'enc_key' not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN enc_key BLOB")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS failed_logins (
            ip TEXT PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0,
            banned INTEGER NOT NULL DEFAULT 0,
            last_attempt TEXT
        );
    """)
    conn.commit()
    conn.close()


# ── User lookup ────────────────────────────────────────────────────────────
def fetch_user_by_id(user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row


def fetch_user_for_login(username):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()
    return row


def insert_user(username, password_hash, enc_key=None):
    conn = _conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, enc_key) VALUES (?,?,?)",
            (username, password_hash, enc_key)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# ── Per-user media encryption key ─────────────────────────────────────────
def get_user_enc_key(user_id):
    """Return the user's raw encryption key bytes, or None if unset."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT enc_key FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if not row or not row[0]:
        return None
    return bytes(row[0])


def get_or_create_user_enc_key(user_id):
    """Return the user's encryption key, lazily generating one on first use.

    Existing users created before per-user encryption was added get a key
    minted the first time they upload a private file.
    """
    existing = get_user_enc_key(user_id)
    if existing:
        return existing
    # Local import to avoid pulling cryptography into the auth module
    # unless we actually need it.
    from ..media.crypto import new_key
    key = new_key()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET enc_key=? WHERE id=?", (key, user_id))
    conn.commit()
    conn.close()
    return key


# ── Failed-login / IP-ban tracking ─────────────────────────────────────────
def is_ip_banned(ip):
    try:
        conn = _conn()
        cur = conn.cursor()
        cur.execute("SELECT banned FROM failed_logins WHERE ip=?", (ip,))
        row = cur.fetchone()
        conn.close()
        return bool(row and row[0])
    except Exception:
        return False


def record_failed_login(ip):
    now = datetime.now().isoformat()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO failed_logins (ip, count, banned, last_attempt)
        VALUES (?, 1, 0, ?)
        ON CONFLICT(ip) DO UPDATE SET
            count = count + 1,
            banned = CASE WHEN count + 1 >= ? THEN 1 ELSE banned END,
            last_attempt = ?
    """, (ip, now, Config.BAN_THRESHOLD, now))
    conn.commit()
    conn.close()


def reset_failed_logins(ip):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM failed_logins WHERE ip=?", (ip,))
    conn.commit()
    conn.close()
