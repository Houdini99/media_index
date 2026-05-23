"""Auth routes, request hooks, and the login_required decorator.

All persistence calls go through app.auth.db — no raw SQL here.
"""
from functools import wraps
from flask import (
    render_template, request, redirect, url_for, flash, session, g, abort
)
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth_bp
from .db import (
    fetch_user_by_id,
    fetch_user_for_login,
    insert_user,
    is_ip_banned,
    record_failed_login,
    reset_failed_logins,
)
from ..config import Config
from ..extensions import limiter


def _client_ip():
    return get_remote_address()


# ── Block permanently banned IPs on every request ─────────────────────────
@auth_bp.before_app_request
def block_banned_ips():
    if is_ip_banned(_client_ip()):
        abort(403)


# ── Load logged-in user onto g for every request ──────────────────────────
@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None
    if user_id:
        row = fetch_user_by_id(user_id)
        if row:
            g.user = {'id': row[0], 'username': row[1]}


# ── login_required decorator (importable by other blueprints) ─────────────
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in.', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


# ── Routes ────────────────────────────────────────────────────────────────
@auth_bp.route('/register', methods=('GET', 'POST'))
@limiter.limit("5 per hour")
def register():
    if not Config.REGISTRATION_OPEN:
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
            # Local import: avoids a circular import via app.media at module load
            # time (auth.routes is imported before app.media is fully initialised).
            from ..media.crypto import new_key
            if insert_user(username, pw_hash, new_key()):
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Username already exists.', 'warning')
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        row = fetch_user_for_login(username)

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

    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=('POST',))
def logout():
    session.clear()
    response = redirect(url_for('auth.login'))
    response.set_cookie(
        key='session',
        value='',
        expires=0,
        secure=True,
        httponly=True,
        samesite='Lax'
    )
    return response
