"""Application factory."""
import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .extensions import csrf, limiter


def create_app():
    Config.validate()

    app = Flask(__name__, static_folder='static', template_folder='templates')

    # ── ProxyFix (preserved verbatim from original main.py) ────────────────
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,    # Trust 1 proxy (NPM)
        x_proto=1,
        x_host=1,
        x_prefix=1
    )

    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER

    # ── Ensure upload/thumb directories exist ──────────────────────────────
    for folder in (Config.UPLOAD_FOLDER, Config.THUMB_FOLDER):
        os.makedirs(folder, exist_ok=True)

    # ── Initialise databases ──────────────────────────────────────────────
    from .auth.db import init_auth_db
    from .media.db import init_media_db
    init_auth_db()
    init_media_db()

    # ── Bind extensions ───────────────────────────────────────────────────
    csrf.init_app(app)
    limiter.init_app(app)

    # ── Register blueprints ───────────────────────────────────────────────
    from .auth import auth_bp
    from .media import media_bp
    from .main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(main_bp)

    # ── Template filter ───────────────────────────────────────────────────
    @app.template_filter('basename')
    def basename_filter(path):
        return os.path.basename(path)

    # ── Security headers (preserved verbatim) ─────────────────────────────
    @app.after_request
    def add_security_headers(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "base-uri 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; "
            "media-src 'self' blob:; "
            "object-src 'none'; "
            "frame-ancestors 'none'; "
            "connect-src 'self'; "
            "font-src 'self';"
        )
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive, nosnippet'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app
