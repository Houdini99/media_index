import os
import sqlite3
import hashlib
import socket
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, flash, send_from_directory, jsonify, session, g
from flask_wtf.csrf import CSRFProtect
from templates import TEMPLATE_INDEX, TEMPLATE_UPLOAD, TEMPLATE_TAGS
from auth import auth_bp, login_required, limiter
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from PIL import Image, ImageSequence
from moviepy import VideoFileClip
import logging
import sys
import tempfile
from logging.handlers import TimedRotatingFileHandler

#---------------------LOGGER---------------------
class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, stream=None, log_level=logging.INFO):
        self.logger = logger
        self.stream = stream
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        # Also write to original stream (console)
        if self.stream:
            self.stream.write(buf)
        
        # Log to file
        temp_linebuf = self.linebuf + buf
        self.linebuf = ''
        for line in temp_linebuf.splitlines(True):
            if line[-1:] == '\n':
                self.logger.log(self.log_level, line.rstrip())
            else:
                self.linebuf += line

    def flush(self):
        if self.linebuf != '':
            self.logger.log(self.log_level, self.linebuf.rstrip())
        self.linebuf = ''
        if self.stream:
            self.stream.flush()

# -------------------- CONFIG --------------------
UPLOAD_FOLDER = 'media_files'
THUMB_FOLDER = 'thumbnails'
DB_FILE = 'media_index.db'
AUTH_DB = 'users.db'
ALLOWED_IMAGE_EXT = {'jpg', 'jpeg', 'png', 'webp', 'heic'}
ALLOWED_GIF_EXT = {'gif'}
ALLOWED_VIDEO_EXT = {'mp4', 'webm', 'avi', 'mov', 'mkv'}
THUMB_SIZE = (150, 150)
PAGE_SIZE = 30
PORT = 5001

# --------------------- INIT ---------------------
for folder in (UPLOAD_FOLDER, THUMB_FOLDER):
    os.makedirs(folder, exist_ok=True)

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filepath TEXT NOT NULL,
        thumb TEXT,
        tags TEXT,
        filehash TEXT UNIQUE,
        uploaded_by INTEGER,
        upload_date TEXT
    );
    """)
    cur.execute("PRAGMA table_info(media)")
    cols = [c[1] for c in cur.fetchall()]
    if 'uploaded_by' not in cols:
        cur.execute("ALTER TABLE media ADD COLUMN uploaded_by INTEGER")
    if 'upload_date' not in cols:
        cur.execute("ALTER TABLE media ADD COLUMN upload_date TEXT")
    conn.commit()
    conn.close()

init_db()

# -------------------- APP SETUP --------------------
app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,    # Trust 1 proxy (NPM)
    x_proto=1,
    x_host=1,
    x_prefix=1
)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024  # 10 GiB
# -------------------- LOGGING SETUP --------------------
# Create log directory
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
os.makedirs(log_dir, exist_ok=True)

# Set up logger for stdout
stdout_logger = logging.getLogger('STDOUT')
stdout_logger.setLevel(logging.INFO)

# Set up logger for stderr  
stderr_logger = logging.getLogger('STDERR')
stderr_logger.setLevel(logging.ERROR)

# Create TimedRotatingFileHandler for daily rotation
log_path = os.path.join(log_dir, "app.log")
stdout_handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1)
stdout_handler.suffix = "%Y-%m-%d"
stdout_formatter = logging.Formatter('%(asctime)s [STDOUT] %(message)s')
stdout_handler.setFormatter(stdout_formatter)

stderr_handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1)
stderr_handler.suffix = "%Y-%m-%d"
stderr_formatter = logging.Formatter('%(asctime)s [STDERR] %(message)s')
stderr_handler.setFormatter(stderr_formatter)

# Add handlers to loggers
stdout_logger.addHandler(stdout_handler)
stderr_logger.addHandler(stderr_handler)

# Redirect stdout and stderr to loggers while keeping console output
sys.stdout = StreamToLogger(stdout_logger, sys.stdout, logging.INFO)
sys.stderr = StreamToLogger(stderr_logger, sys.stderr, logging.ERROR)
#----------------------LOGGER-------------------------
_secret = os.environ.get('SECRET_KEY')
if not _secret:
    raise RuntimeError("SECRET_KEY environment variable is not set. Copy .env.example to .env and generate a strong random value.")
app.secret_key = _secret
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(
    SESSION_COOKIE_SECURE=os.environ.get('DEV_MODE', '').lower() != 'true',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
csrf = CSRFProtect(app)
# Register auth blueprint
app.register_blueprint(auth_bp)

# Configure Redis for rate limiting
limiter.init_app(app)

# -------------------- UTILS --------------------
def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return ext in (ALLOWED_IMAGE_EXT | ALLOWED_GIF_EXT | ALLOWED_VIDEO_EXT)

def file_type(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext in ALLOWED_IMAGE_EXT:
        return "image"
    if ext in ALLOWED_GIF_EXT:
        return "gif"
    if ext in ALLOWED_VIDEO_EXT:
        return "video"
    return "unknown"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def gen_image_thumb(src, dst):
    try:
        img = Image.open(src)
        if img.format == 'GIF':
            frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
            frame = frames[0]
            frame.thumbnail(THUMB_SIZE)
            frame.save(dst, format='PNG')
        else:
            img.thumbnail(THUMB_SIZE)
            img.save(dst, format='PNG')
        return dst
    except Exception:
        return gen_placeholder_thumb(dst)

def gen_video_thumb(src, dst):
    clip = None
    try:
        clip = VideoFileClip(src)
        dur = clip.duration
        for t in (2, dur/2, 1, dur/3):
            if 0 <= t <= dur:
                try:
                    frame = clip.get_frame(t)
                    img = Image.fromarray(frame)
                    img.thumbnail(THUMB_SIZE)
                    img.save(dst, format='PNG')
                    break
                except Exception:
                    continue
        else:
            frame = clip.get_frame(min(0.1, dur))
            img = Image.fromarray(frame)
            img.thumbnail(THUMB_SIZE)
            img.save(dst, format='PNG')
        return dst
    except Exception:
        return gen_placeholder_thumb(dst)
    finally:
        if clip:
            try:
                clip.reader.close()
            except Exception:
                pass
            if hasattr(clip, 'audio') and clip.audio:
                try:
                    clip.audio.reader.close_proc()
                except Exception:
                    pass

def gen_placeholder_thumb(dst):
    img = Image.new('RGB', THUMB_SIZE, (32, 48, 32))
    img.save(dst, format='PNG')
    return dst

def get_username_by_id(uid):
    if not uid:
        return None
    try:
        conn = sqlite3.connect(AUTH_DB)
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE id=?", (uid,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None
    except Exception as e:
        logging.warning("get_username_by_id failed for uid=%s: %s", uid, e)
        return None

def get_usernames_for_media(data):
    ids = {m[5] for m in data if len(m)>5 and m[5]}
    if not ids:
        return {}
    try:
        conn = sqlite3.connect(AUTH_DB)
        cur = conn.cursor()
        ph = ','.join('?'*len(ids))
        cur.execute(f"SELECT id,username FROM users WHERE id IN ({ph})", list(ids))
        um = {uid: name for uid, name in cur.fetchall()}
        conn.close()
        return um
    except Exception as e:
        logging.warning("get_usernames_for_media failed: %s", e)
        return {}

def _build_where(ft, search, exclude_tags):
    """Build shared WHERE clause components for media queries."""
    conds, params = [], []
    if ft and ft != 'all':
        if ft == 'image':
            conds.append("(" + " OR ".join(f"filepath LIKE '%.{e}'" for e in ALLOWED_IMAGE_EXT) + ")")
        elif ft == 'video':
            conds.append("(" + " OR ".join(f"filepath LIKE '%.{e}'" for e in ALLOWED_VIDEO_EXT) + ")")
        elif ft == 'gif':
            conds.append("filepath LIKE '%.gif'")
    if search:
        conds.append("tags LIKE ?")
        params.append(f"%{search}%")
    if exclude_tags:
        for tag in [t.strip() for t in exclude_tags.split(',') if t.strip()]:
            # Match whole tag only by padding the stored tags with commas on both sides,
            # so "ai" won't match "portainer" or any other tag that merely contains the word.
            conds.append("(tags IS NULL OR (',' || tags || ',') NOT LIKE ?)")
            params.append(f"%,{tag},%")
    return conds, params

def get_media_count(ft=None, search=None, exclude_tags=None):
    conds, params = _build_where(ft, search, exclude_tags)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    q = "SELECT COUNT(*) FROM media"
    if conds:
        q += " WHERE " + " AND ".join(conds)
    cur.execute(q, params)
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_media(ft=None, search=None, exclude_tags=None, page=1):
    conds, params = _build_where(ft, search, exclude_tags)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    q = "SELECT * FROM media"
    if conds:
        q += " WHERE " + " AND ".join(conds)
    q += " ORDER BY id DESC"
    q += f" LIMIT {PAGE_SIZE} OFFSET {(page - 1) * PAGE_SIZE}"
    cur.execute(q, params)
    data = cur.fetchall()
    conn.close()

    umap = get_usernames_for_media(data)
    enhanced = []
    for m in data:
        lst = list(m)
        uname = umap.get(m[5], 'Unknown')
        lst.append(uname)
        enhanced.append(tuple(lst))

    return enhanced

def delete_media(mid, user_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT filepath,thumb,uploaded_by FROM media WHERE id=?", (mid,))
    row = cur.fetchone()
    if not row:
        conn.close(); return False
    if row[2] != user_id:
        conn.close(); return False
    for p in row[:2]:
        if p and os.path.exists(p):
            os.remove(p)
    cur.execute("DELETE FROM media WHERE id=?", (mid,))
    conn.commit()
    conn.close()
    return True

def insert_media(fp, th, tags, fh, uid):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        udate = datetime.now().isoformat()
        uname = get_username_by_id(uid)
        if uname and f"user:{uname}" not in (tags or ""):
            tags = f"{tags},user:{uname}" if tags else f"user:{uname}"
        cur.execute(
            "INSERT INTO media (filepath,thumb,tags,filehash,uploaded_by,upload_date) VALUES (?,?,?,?,?,?)",
            (fp, th, tags, fh, uid, udate)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_tag_statistics():
    """Get all tags and their counts from the database"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Get all media with tags
    cur.execute("SELECT tags FROM media WHERE tags IS NOT NULL AND tags != ''")
    rows = cur.fetchall()
    conn.close()
    
    tag_counts = {}
    
    # Process each row's tags
    for (tags_str,) in rows:
        if tags_str:
            # Split by comma and clean up each tag
            tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Sort by count (descending) then by tag name
    sorted_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0].lower()))
    
    return sorted_tags

# --------------------- ROUTES -------------------
@app.route('/')
@login_required
def index():
    hide_ai = request.args.get('hide_ai', '')
    exclude_tags = request.args.get('exclude_tags', '')
    if hide_ai == '1':
        ai_tags = 'fake,ai,grok,deepfake,gemini'
        exclude_tags = (exclude_tags + ',' + ai_tags).strip(',') if exclude_tags else ai_tags
    media = get_media(
        request.args.get('type', 'all'),
        request.args.get('search', ''),
        exclude_tags
    )
    return render_template_string(
        TEMPLATE_INDEX,
        media=media,
        search=request.args.get('search', ''),
        exclude_tags=request.args.get('exclude_tags', ''),
        filter_type=request.args.get('type', 'all'),
        hide_ai=hide_ai
    )

@app.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    if request.method=='POST':
        files = request.files.getlist('files')
        results = {'uploaded':[], 'duplicates':[], 'errors':[]}
        uid = g.user['id'] if g.user else None
        if not uid:
            flash("❌ Fehler: Nicht eingeloggt.","danger")
            return redirect(url_for('upload'))
        for i, f in enumerate(files):
            fn = secure_filename(f.filename)
            if not fn or not allowed_file(fn):
                results['errors'].append(fn); continue
            tags = request.form.get(f'tags_{i}','')
            ext = fn.rsplit('.',1)[-1].lower()
            with tempfile.NamedTemporaryFile(dir=UPLOAD_FOLDER, delete=False, suffix=f'.{ext}') as tf:
                tmp = tf.name
            f.save(tmp)
            fh = sha256_file(tmp)
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("SELECT id FROM media WHERE filehash=?", (fh,))
            if cur.fetchone():
                conn.close(); os.remove(tmp)
                results['duplicates'].append(fn); continue
            conn.close()
            final = os.path.join(UPLOAD_FOLDER, f"{fh}.{ext}")
            os.rename(tmp, final)
            tname = f"{fh}.png"
            tpath = os.path.join(THUMB_FOLDER, tname)
            if ext in ALLOWED_IMAGE_EXT|ALLOWED_GIF_EXT:
                gen_image_thumb(final, tpath)
            elif ext in ALLOWED_VIDEO_EXT:
                gen_video_thumb(final, tpath)
            else:
                gen_placeholder_thumb(tpath)
            if insert_media(final, tpath, ','.join(filter(None,[tags,file_type(fn)])), fh, uid):
                results['uploaded'].append(fn)
            else:
                results['errors'].append(fn)
        for k,v in results.items():
            if v:
                if k=='uploaded':
                    flash(f"✅Successful: {', '.join(v)}","success")
                elif k=='duplicates':
                    flash(f"⚠️ Duplicates: {', '.join(v)}","warning")
                else:
                    flash(f"❌ Error: {', '.join(v)}","danger")
        return redirect(url_for('upload'))
    return render_template_string(TEMPLATE_UPLOAD)

def update_media_tags(mid, new_tags, user_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        cur.execute("UPDATE media SET tags=? WHERE id=? AND uploaded_by=?", (new_tags, mid, user_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()

@app.route('/thumbs/<fname>')
@login_required
def serve_thumb(fname):
    return send_from_directory(THUMB_FOLDER, fname)

@app.route('/media/<fname>')
@login_required
def serve_media(fname):
    return send_from_directory(UPLOAD_FOLDER, fname)

@app.route('/mediadata/<int:media_id>')
@login_required
def media_meta(media_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM media WHERE id=?", (media_id,))
    m = cur.fetchone()
    conn.close()
    if m:
        uid = m[5]
        return jsonify({
            'id': m[0],
            'filepath': url_for('serve_media', fname=os.path.basename(m[1])),
            'thumb': url_for('serve_thumb', fname=os.path.basename(m[2])),
            'tags': m[3],
            'type': file_type(m[1]),
            'uploaded_by': get_username_by_id(uid) or 'Unknown',
            'upload_date': m[6]
        })
    return jsonify({'error':'Not found'}),404

@app.route('/delete/<int:media_id>', methods=['POST'])
@login_required
def delete(media_id):
    if delete_media(media_id, g.user['id']):
        flash("✅ File deleted.","success")
    else:
        flash("❌ Error deleting file.","danger")
    return redirect(url_for('index'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static','favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /\n", 200, {'Content-Type':'text/plain'}

@app.route('/api/media')
@login_required
def api_media():
    ft = request.args.get('type', 'all')
    search = request.args.get('search', '')
    hide_ai = request.args.get('hide_ai', '')
    exclude_tags = request.args.get('exclude_tags', '')
    if hide_ai == '1':
        ai_tags = 'fake,ai,grok,deepfake,gemini,chatgpt'
        exclude_tags = (exclude_tags + ',' + ai_tags).strip(',') if exclude_tags else ai_tags
    try:
        page = max(1, min(int(request.args.get('page', 1)), 9999))
    except (ValueError, TypeError):
        page = 1
    media = get_media(ft, search, exclude_tags, page)
    total = get_media_count(ft, search, exclude_tags)
    has_more = (page * PAGE_SIZE) < total
    result = [
        {'id': m[0], 'thumb': os.path.basename(m[2]), 'tags': m[3] or '', 'type': file_type(m[1])}
        for m in media
    ]
    return jsonify({'media': result, 'has_more': has_more})

@app.route('/api/tags')
@login_required
def api_tags():
    tag_stats = get_tag_statistics()
    return jsonify(sorted(tag for tag, _ in tag_stats))

@app.route('/tags')
@login_required
def tags():
    """Show tag statistics page"""
    tag_stats = get_tag_statistics()
    
    # Calculate some statistics
    total_tags = len(tag_stats)
    total_usages = sum(count for _, count in tag_stats)
    
    return render_template_string(
        TEMPLATE_TAGS,
        tag_stats=tag_stats,
        total_tags=total_tags,
        total_usages=total_usages
    )


@app.route('/edit/<int:media_id>', methods=['POST'])
@login_required
def edit_tags(media_id):
    new_tags = request.form.get('tags', '').strip()
    if update_media_tags(media_id, new_tags, g.user['id']):
        flash("✅ Tags successfully updated.", "success")
    else:
        flash("❌ Error updating tags.", "danger")
    return redirect(url_for('index'))

@app.template_filter('basename')
def basename_filter(path):
    return os.path.basename(path)

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

    # Cache-Control fÃ¼r alle Antworten
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Pragma']        = 'no-cache'

    response.headers['X-Robots-Tag']          = 'noindex, nofollow, noarchive, nosnippet'
    response.headers['X-Frame-Options']        = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['X-XSS-Protection']       = '1; mode=block'
    return response

if __name__ == '__main__':
    print(f"Starting MediaIndex on http://{get_lan_ip()}:{PORT}/")
    app.run(host="0.0.0.0", port=PORT, debug=False)
