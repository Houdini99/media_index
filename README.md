# MediaIndex

A self-hosted media management app for organizing, browsing, and tagging images, GIFs, and videos. Built with Flask, it features user authentication, tag-based search, automatic thumbnail generation, and a dark-themed responsive UI.

## Features

- **Multi-format support** — images (jpg, jpeg, png, webp, heic), GIFs, and videos (mp4, webm, avi, mov, mkv)
- **Automatic thumbnails** — generated from images, GIF first frames, and video frames
- **Duplicate detection** — SHA256 hash prevents storing the same file twice
- **Tag system** — comma-separated tags, per-file editing, tag statistics page
- **User accounts** — registration/login with bcrypt password hashing and rate-limited login (5/min)
- **Search & filter** — filter by type, search by tag, exclude tags (e.g. hide AI content)
- **Infinite scroll gallery** — paginated API with JS-driven infinite scroll
- **Security headers** — HSTS, CSP, X-Frame-Options, Referrer-Policy, etc.
- **Reverse-proxy ready** — ProxyFix middleware trusts one upstream proxy (e.g. Nginx Proxy Manager)
- **Docker support** — single `docker compose up` deployment

<p align="center">
  <img src="preview.png" alt="Description" width="600">
</p>

## Requirements

- Docker & Docker Compose (recommended), **or**
- Python 3.11+, FFmpeg, Redis

## Quick Start (Docker)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/media-index.git
cd media-index
```

### 2. Create the environment file

```bash
cp .env.example .env
```

Edit `.env` and set a strong `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the output as the value of `SECRET_KEY` in `.env`.

### 3. Create data directories and empty database files

Docker bind-mounts require the host paths to exist before the container starts:

```bash
mkdir -p media_files thumbnails log
touch media_index.db users.db
```

### 4. Start the stack

```bash
docker compose up -d
```

The app will be available at `http://localhost:5001` (or whatever `PORT` you set in `.env`).

### 5. Register the first user

Open the app in your browser and navigate to `/register` to create your account. To disable public registration after setup, set `REGISTRATION_OPEN = False` in `auth.py` and restart the container.

---

## Manual Deployment (without Docker)

### Prerequisites

- Python 3.11+
- FFmpeg installed system-wide (`sudo apt install ffmpeg` / `brew install ffmpeg`)
- Redis running on `localhost:6379` (or set `REDIS_URL` in your environment)

### Setup

```bash
git clone https://github.com/your-username/media-index.git
cd media-index

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configure environment

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY and optionally DEV_MODE, REDIS_URL
export $(grep -v '^#' .env | xargs)
```

### Run

```bash
flask run --host=0.0.0.0 --port=5001
```

For production, use a WSGI server (Gunicorn):

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 main:app
```

---

## Reverse Proxy (Nginx / Nginx Proxy Manager)

The app trusts one upstream proxy via `ProxyFix`. Point your proxy to `http://<host>:5001` and ensure it forwards the standard `X-Forwarded-*` headers.

Example Nginx location block:

```nginx
location / {
    proxy_pass         http://127.0.0.1:5001;
    proxy_set_header   Host              $host;
    proxy_set_header   X-Real-IP         $remote_addr;
    proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
    client_max_body_size 10G;
}
```

---

## Configuration Reference

All runtime configuration is done via environment variables (or the `.env` file when using Docker Compose).

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | *(required)* | Flask session signing key. Generate with `secrets.token_hex(32)`. |
| `DEV_MODE` | `false` | Set to `true` in local dev to disable HTTPS-only session cookies. |
| `REDIS_URL` | `redis://redis:6379` | Redis connection URI used by the rate limiter. |
| `PORT` | `5001` | Host port exposed by Docker Compose. |

Constants inside `main.py` (edit the file to change them):

| Constant | Default | Description |
|----------|---------|-------------|
| `UPLOAD_FOLDER` | `media_files` | Directory for uploaded files. |
| `THUMB_FOLDER` | `thumbnails` | Directory for generated thumbnails. |
| `THUMB_SIZE` | `(150, 150)` | Thumbnail dimensions in pixels. |
| `PAGE_SIZE` | `30` | Items per page in the gallery. |
| `PORT` | `5001` | Port the Flask app listens on. |

To disable user registration, set `REGISTRATION_OPEN = False` in `auth.py`.

---

## Project Structure

```
media-index/
├── main.py            # Flask app, routes, media logic
├── auth.py            # Auth blueprint, login/register, rate limiting
├── templates.py       # All HTML templates (inline Jinja2 + CSS + JS)
├── requirements.txt   # Python dependencies
├── Dockerfile
├── docker-compose.yml
├── .env.example       # Environment variable template
├── .gitignore
├── media_files/       # Uploaded media (excluded from git)
├── thumbnails/        # Generated thumbnails (excluded from git)
├── log/               # Rotating log files (excluded from git)
├── media_index.db     # Media SQLite database (excluded from git)
└── users.db           # User SQLite database (excluded from git)
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Gallery page |
| `GET/POST` | `/upload` | Upload media files |
| `POST` | `/delete/<id>` | Delete a media item (owner only) |
| `POST` | `/edit/<id>` | Update tags on a media item (owner only) |
| `GET` | `/tags` | Tag statistics page |
| `GET` | `/api/media` | JSON list of media (supports `type`, `search`, `exclude_tags`, `hide_ai`, `page`) |
| `GET` | `/api/tags` | JSON list of all tags |
| `GET` | `/mediadata/<id>` | JSON metadata for a single media item |
| `GET` | `/login` | Login page |
| `GET` | `/register` | Registration page |
| `GET` | `/logout` | Logout |

---

## Tech Stack

- **Backend**: Python 3.11, Flask, Flask-WTF (CSRF), Flask-Limiter
- **Storage**: SQLite (media & users), local filesystem (files & thumbnails)
- **Cache / Rate Limiting**: Redis
- **Image processing**: Pillow
- **Video processing**: moviepy + FFmpeg
- **Frontend**: Vanilla JS, CSS custom properties, dark theme

## License

MIT
