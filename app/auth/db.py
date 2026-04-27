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
            password_hash TEXT NOT NULL
        );
    """)
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


def insert_user(username, password_hash):
    conn = _conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?,?)",
            (username, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


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
