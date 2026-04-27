"""Environment-driven configuration.

All values are read from environment variables — no hardcoded secrets,
no standalone config dictionary checked into the repo.
"""
import os

# Project root: directory containing run.py and the app/ package.
# /app/app/config.py → dirname = /app/app → dirname = /app
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    # Filesystem locations — absolute, anchored at PROJECT_ROOT so they don't
    # depend on the process working directory or Flask's app.root_path.
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'media_files')
    THUMB_FOLDER = os.path.join(PROJECT_ROOT, 'thumbnails')
    DB_FILE = os.path.join(PROJECT_ROOT, 'media_index.db')
    AUTH_DB = os.path.join(PROJECT_ROOT, 'users.db')

    # File-type allow-lists
    ALLOWED_IMAGE_EXT = {'jpg', 'jpeg', 'png', 'webp', 'heic'}
    ALLOWED_GIF_EXT = {'gif'}
    ALLOWED_VIDEO_EXT = {'mp4', 'webm', 'avi', 'mov', 'mkv'}

    # Behaviour
    THUMB_SIZE = (150, 150)
    PAGE_SIZE = 30
    PORT = int(os.environ.get('PORT', 5001))
    BAN_THRESHOLD = 10
    REGISTRATION_OPEN = True

    # Flask
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024 * 1024  # 10 GiB

    # Sourced from environment
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    DEV_MODE = os.environ.get('DEV_MODE', '').lower() == 'true'

    # Cookie hardening — secure cookies off only in DEV_MODE
    SESSION_COOKIE_SECURE = not DEV_MODE
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    @staticmethod
    def validate():
        if not Config.SECRET_KEY:
            raise RuntimeError(
                "SECRET_KEY environment variable is not set. "
                "Copy .env.example to .env and generate a strong random value."
            )
