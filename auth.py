# auth.py
import os
import sqlite3
from datetime import datetime
from flask import (
    Blueprint, render_template_string, request,
    redirect, url_for, flash, session, g, abort
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash

AUTH_DB = 'users.db'
BAN_THRESHOLD = 10  # permanent IP ban after this many failed logins
auth_bp = Blueprint('auth', __name__)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.environ.get("REDIS_URL", "redis://localhost:6379")
)
REGISTRATION_OPEN = True  # set to True temporarily to create your account, then set back to False
# DB initializing
def init_auth_db():
    conn = sqlite3.connect(AUTH_DB)
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

init_auth_db()

def _client_ip():
    return get_remote_address()

def is_ip_banned(ip):
    try:
        conn = sqlite3.connect(AUTH_DB)
        cur = conn.cursor()
        cur.execute("SELECT banned FROM failed_logins WHERE ip=?", (ip,))
        row = cur.fetchone()
        conn.close()
        return bool(row and row[0])
    except Exception:
        return False

def record_failed_login(ip):
    now = datetime.now().isoformat()
    conn = sqlite3.connect(AUTH_DB)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO failed_logins (ip, count, banned, last_attempt)
        VALUES (?, 1, 0, ?)
        ON CONFLICT(ip) DO UPDATE SET
            count = count + 1,
            banned = CASE WHEN count + 1 >= ? THEN 1 ELSE banned END,
            last_attempt = ?
    """, (ip, now, BAN_THRESHOLD, now))
    conn.commit()
    conn.close()

def reset_failed_logins(ip):
    conn = sqlite3.connect(AUTH_DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM failed_logins WHERE ip=?", (ip,))
    conn.commit()
    conn.close()

# Block permanently banned IPs on every request
@auth_bp.before_app_request
def block_banned_ips():
    if is_ip_banned(_client_ip()):
        abort(403)

# Help function: Append to current request
@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None
    if user_id:
        conn = sqlite3.connect(AUTH_DB)
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            g.user = {'id': row[0], 'username': row[1]}

# Registration
@auth_bp.route('/register', methods=('GET','POST'))
@limiter.limit("5 per hour")
def register():
    if not REGISTRATION_OPEN:
        flash('Registration is temporarily closed.', 'warning')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash('Username and password are required.', 'danger')
        elif len(password) < 8:
            flash('The password must be at least 8 characters long.', 'danger')
        else:
            pw_hash = generate_password_hash(password)
            try:
                conn = sqlite3.connect(AUTH_DB)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?,?)",
                    (username, pw_hash)
                )
                conn.commit()
                conn.close()
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('auth.login'))
            except sqlite3.IntegrityError:
                flash('Username already exists.', 'warning')
    return render_template_string(REG_TEMPLATE)

# Login
@auth_bp.route('/login', methods=('GET','POST'))
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        conn = sqlite3.connect(AUTH_DB)
        cur = conn.cursor()
        cur.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        conn.close()
        
        if row and check_password_hash(row[1], password):
            reset_failed_logins(_client_ip())
            session.clear()
            session['user_id'] = row[0]
            flash(f'Welcome, {username}!', 'success')
            return redirect('/')
        else:
            record_failed_login(_client_ip())
            if is_ip_banned(_client_ip()):
                abort(403)
            flash('Invalid login credentials.', 'danger')
    
    return render_template_string(LOGIN_TEMPLATE)


@auth_bp.route('/logout', methods=('POST',))
def logout():
    session.clear()
    response = redirect(url_for('auth.login'))
    response.set_cookie(
        key='session',        # or your SESSION_COOKIE_NAME
        value='',
        expires=0,
        secure=True,
        httponly=True,
        samesite='Lax'
    )
    return response

# Check the protected route before each call
def login_required(view):
    from functools import wraps
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in.', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# Templates
_AUTH_CSS = """
    :root {
        --bg:          #020408;
        --surface:     #0c1018;
        --surf2:       #131920;
        --surf3:       #1a2230;
        --border:      rgba(255,255,255,.07);
        --border2:     rgba(255,255,255,.12);
        --border-hi:   rgba(124,106,255,.55);
        --text:        #e8edf5;
        --text2:       #a8b3c2;
        --muted:       #58687a;
        --accent:      #7c6aff;
        --accent2:     #5b4de8;
        --success:     #3fb950;
        --danger:      #f85149;
        --warning:     #d29922;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { color-scheme: dark; }
    body {
        background: var(--bg);
        background-image:
            radial-gradient(ellipse 120% 60% at 50% -10%,
                rgba(109,81,255,.16) 0%, transparent 55%),
            radial-gradient(ellipse 60% 40% at 80% 100%,
                rgba(168,85,247,.07) 0%, transparent 50%);
        color: var(--text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
        min-height: 100vh;
        display: flex; align-items: center; justify-content: center;
        padding: 1.5rem;
        -webkit-font-smoothing: antialiased;
    }
    .auth-wrap {
        width: 100%;
        max-width: 400px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }
    /* Brand */
    .auth-brand {
        display: flex;
        align-items: center;
        gap: .6rem;
        text-decoration: none;
        color: var(--text);
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: -.025em;
    }
    .auth-brand-mark {
        width: 32px; height: 32px;
        background: linear-gradient(145deg, #8b7bff 0%, #5b4de8 55%, #a855f7 100%);
        border-radius: 9px;
        display: flex; align-items: center; justify-content: center;
        font-size: .85rem; font-weight: 900; color: #fff;
        box-shadow: 0 0 20px rgba(124,106,255,.5), 0 2px 10px rgba(0,0,0,.6);
    }
    .auth-brand-name {
        background: linear-gradient(90deg, var(--text) 0%, var(--text2) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    /* Card */
    .auth-card {
        width: 100%;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem 2rem 1.75rem;
        box-shadow: 0 24px 64px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.04);
    }
    .auth-title {
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -.03em;
        margin-bottom: .3rem;
        color: var(--text);
    }
    .auth-subtitle {
        font-size: .845rem;
        color: var(--muted);
        margin-bottom: 1.5rem;
    }
    /* Flash */
    .flash {
        display: flex;
        align-items: center;
        gap: .5rem;
        padding: .65rem .85rem;
        margin-bottom: .5rem;
        border-radius: 8px;
        font-size: .83rem;
        border: 1px solid;
        animation: fadeIn .2s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-4px); }
        to   { opacity: 1; transform: none; }
    }
    .flash-success { background: rgba(63,185,80,.07);  border-color: rgba(63,185,80,.22);  color: var(--success); }
    .flash-warning { background: rgba(210,153,34,.07); border-color: rgba(210,153,34,.22); color: var(--warning); }
    .flash-danger  { background: rgba(248,81,73,.07);  border-color: rgba(248,81,73,.22);  color: var(--danger);  }
    /* Fields */
    .field { margin-bottom: .85rem; }
    .field label {
        display: block;
        font-size: .78rem;
        color: var(--muted);
        margin-bottom: .38rem;
        font-weight: 600;
        letter-spacing: .02em;
        text-transform: uppercase;
    }
    .field input {
        width: 100%;
        background: var(--surf2);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 9px;
        padding: .6rem .85rem;
        font-size: .9rem;
        font-family: inherit;
        transition: border-color .15s, box-shadow .15s, background .15s;
    }
    .field input::placeholder { color: var(--muted); }
    .field input:focus {
        outline: none;
        border-color: var(--border-hi);
        box-shadow: 0 0 0 3px rgba(124,106,255,.12);
        background: var(--surf3);
    }
    /* Submit */
    .submit-btn {
        width: 100%;
        padding: .7rem;
        margin-top: .5rem;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
        color: #fff;
        border: none;
        border-radius: 9px;
        font-size: .95rem;
        font-weight: 600;
        cursor: pointer;
        font-family: inherit;
        letter-spacing: -.01em;
        box-shadow: 0 0 0 1px rgba(124,106,255,.25), 0 4px 14px rgba(124,106,255,.2);
        transition: all .18s;
    }
    .submit-btn:hover {
        filter: brightness(1.08);
        box-shadow: 0 0 0 1px rgba(124,106,255,.45), 0 6px 22px rgba(124,106,255,.32);
        transform: translateY(-1px);
    }
    .submit-btn:active { transform: none; filter: brightness(.96); }
    /* Footer */
    .auth-footer {
        text-align: center;
        margin-top: 1.35rem;
        font-size: .82rem;
        color: var(--muted);
    }
    .auth-footer a {
        color: var(--accent);
        text-decoration: none;
        font-weight: 500;
        transition: color .15s;
    }
    .auth-footer a:hover { color: #a89bff; text-decoration: underline; text-underline-offset: 2px; }
    /* Divider */
    .auth-divider {
        width: 100%;
        height: 1px;
        background: var(--border);
        margin: 1.25rem 0;
    }
"""

LOGIN_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8"/>
  <title>MediaIndex — Sign In</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>""" + _AUTH_CSS + """</style>
</head>
<body>
  <div class="auth-wrap">
    <a class="auth-brand" href="#">
      <span class="auth-brand-mark">M</span>
      <span class="auth-brand-name">MediaIndex</span>
    </a>
    <div class="auth-card">
      <div class="auth-title">Welcome back</div>
      <div class="auth-subtitle">Sign in with your account</div>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% for cat, msg in messages %}
          <div class="flash flash-{{cat}}">{{msg}}</div>
        {% endfor %}
      {% endwith %}
      <form method="post">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        <div class="field">
          <label for="username">Username</label>
          <input id="username" name="username" placeholder="Enter username" required autocomplete="username">
        </div>
        <div class="field">
          <label for="password">Password</label>
          <input id="password" name="password" type="password" placeholder="Enter password" required autocomplete="current-password">
        </div>
        <button class="submit-btn" type="submit">Sign In</button>
      </form>
      <div class="auth-divider"></div>
      <div class="auth-footer">
        Don't have an account? <a href="{{ url_for('auth.register') }}">Register</a>
      </div>
    </div>
  </div>
</body>
</html>
"""

REG_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8"/>
  <title>MediaIndex — Register</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>""" + _AUTH_CSS + """</style>
</head>
<body>
  <div class="auth-wrap">
    <a class="auth-brand" href="#">
      <span class="auth-brand-mark">M</span>
      <span class="auth-brand-name">MediaIndex</span>
    </a>
    <div class="auth-card">
      <div class="auth-title">Create Account</div>
      <div class="auth-subtitle">Choose a username and password</div>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% for cat, msg in messages %}
          <div class="flash flash-{{cat}}">{{msg}}</div>
        {% endfor %}
      {% endwith %}
      <form method="post">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        <div class="field">
          <label for="username">Username</label>
          <input id="username" name="username" placeholder="Choose a username" required autocomplete="username">
        </div>
        <div class="field">
          <label for="password">Password</label>
          <input id="password" name="password" type="password" placeholder="Choose a secure password" required minlength="8" autocomplete="new-password">
        </div>
        <button class="submit-btn" type="submit">Create Account</button>
      </form>
      <div class="auth-divider"></div>
      <div class="auth-footer">
        Already have an account? <a href="{{ url_for('auth.login') }}">Sign In</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
