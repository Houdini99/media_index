# ---------------------------------------------------------------------------
#  Shared CSS
# ---------------------------------------------------------------------------
_COMMON_CSS = """
    :root {
        --bg:           #020408;
        --bg2:          #060a12;
        --surface:      #0c1018;
        --surf2:        #131920;
        --surf3:        #1a2230;
        --border:       rgba(255,255,255,.07);
        --border2:      rgba(255,255,255,.12);
        --border-hi:    rgba(124,106,255,.55);
        --text:         #e8edf5;
        --text2:        #a8b3c2;
        --muted:        #58687a;
        --accent:       #7c6aff;
        --accent2:      #5b4de8;
        --accent-glow:  rgba(124,106,255,.35);
        --success:      #3fb950;
        --danger:       #f85149;
        --warning:      #d29922;
        --r:            12px;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html {
        color-scheme: dark;
        scroll-behavior: smooth;
    }

    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--surf3); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--muted); }

    body {
        background: var(--bg);
        background-image:
            radial-gradient(ellipse 100% 40% at 50% 0%,
                rgba(109,81,255,.13) 0%,
                transparent 60%);
        color: var(--text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
        font-size: 15px;
        line-height: 1.6;
        min-height: 100vh;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* ── NAVIGATION ─────────────────────────────────────────────────────── */
    nav {
        height: 58px;
        background: rgba(2,4,8,.88);
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        padding: 0 1.75rem;
        gap: .75rem;
        position: sticky;
        top: 0;
        z-index: 50;
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
    }

    .brand {
        font-weight: 700;
        font-size: .9rem;
        color: var(--text);
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: .55rem;
        letter-spacing: -.025em;
        flex-shrink: 0;
        transition: opacity .15s;
    }
    .brand:hover { opacity: .75; }

    .brand-mark {
        width: 28px; height: 28px;
        background: linear-gradient(145deg, #8b7bff 0%, #5b4de8 55%, #a855f7 100%);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: .78rem; font-weight: 900; color: #fff;
        box-shadow: 0 0 18px rgba(124,106,255,.5), 0 2px 8px rgba(0,0,0,.6);
        flex-shrink: 0;
        letter-spacing: 0;
    }

    .brand-name {
        background: linear-gradient(90deg, var(--text) 0%, var(--text2) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .nav-sep {
        width: 1px; height: 18px;
        background: var(--border);
        flex-shrink: 0;
        margin: 0 .25rem;
    }

    .nav-links {
        display: flex;
        gap: .1rem;
        flex: 1;
    }

    .nav-links a {
        position: relative;
        color: var(--muted);
        text-decoration: none;
        font-size: .82rem;
        font-weight: 500;
        padding: .38rem .75rem;
        border-radius: 7px;
        transition: color .15s, background .15s;
        letter-spacing: -.01em;
    }
    .nav-links a:hover  { color: var(--text2); background: rgba(255,255,255,.04); }
    .nav-links a.active { color: var(--text);  background: rgba(255,255,255,.06); }
    .nav-links a.active::after {
        content: '';
        position: absolute;
        bottom: -1px; left: 50%;
        transform: translateX(-50%);
        width: 18px; height: 2px;
        background: linear-gradient(90deg, var(--accent), #a855f7);
        border-radius: 99px;
        box-shadow: 0 0 8px var(--accent-glow);
    }

    .nav-right {
        display: flex;
        align-items: center;
        gap: .6rem;
        flex-shrink: 0;
    }

    .user-chip {
        display: flex;
        align-items: center;
        gap: .45rem;
        padding: .28rem .65rem .28rem .38rem;
        background: var(--surf2);
        border: 1px solid var(--border);
        border-radius: 99px;
        font-size: .8rem;
        color: var(--text2);
        letter-spacing: -.01em;
        transition: border-color .15s;
    }
    .user-chip:hover { border-color: var(--border2); }

    .user-avatar {
        width: 20px; height: 20px;
        background: linear-gradient(135deg, var(--accent), #a855f7);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: .62rem; font-weight: 800; color: #fff;
        flex-shrink: 0;
    }

    .nav-logout {
        color: var(--danger);
        text-decoration: none;
        font-weight: 500;
        font-size: .78rem;
        padding: .3rem .6rem;
        border: 1px solid rgba(248,81,73,.18);
        border-radius: 7px;
        transition: all .15s;
        white-space: nowrap;
        letter-spacing: -.01em;
    }
    .nav-logout:hover {
        background: rgba(248,81,73,.1);
        border-color: rgba(248,81,73,.4);
        color: #ff7b72;
    }

    /* ── LAYOUT ─────────────────────────────────────────────────────────── */
    .container {
        max-width: 1480px;
        margin: 0 auto;
        padding: 1.75rem 1.5rem;
    }

    /* ── FLASH MESSAGES ─────────────────────────────────────────────────── */
    .flashes { margin-bottom: 1.25rem; display: flex; flex-direction: column; gap: .4rem; }

    .flash {
        display: flex;
        align-items: center;
        gap: .6rem;
        padding: .7rem 1rem;
        border-radius: 9px;
        font-size: .845rem;
        border: 1px solid;
        animation: fadeSlide .22s ease;
    }
    @keyframes fadeSlide {
        from { opacity: 0; transform: translateY(-5px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .flash-icon {
        width: 18px; height: 18px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: .65rem; font-weight: 900; flex-shrink: 0;
    }
    .flash-success { background: rgba(63,185,80,.07); border-color: rgba(63,185,80,.22); color: var(--success); }
    .flash-success .flash-icon { background: rgba(63,185,80,.15); color: var(--success); }
    .flash-warning { background: rgba(210,153,34,.07); border-color: rgba(210,153,34,.22); color: var(--warning); }
    .flash-warning .flash-icon { background: rgba(210,153,34,.15); color: var(--warning); }
    .flash-danger  { background: rgba(248,81,73,.07);  border-color: rgba(248,81,73,.22);  color: var(--danger);  }
    .flash-danger  .flash-icon { background: rgba(248,81,73,.15);  color: var(--danger);  }

    /* ── BUTTONS ─────────────────────────────────────────────────────────── */
    .btn {
        display: inline-flex;
        align-items: center;
        gap: .4rem;
        padding: .5rem 1.1rem;
        border-radius: 8px;
        font-size: .845rem;
        font-weight: 500;
        cursor: pointer;
        border: none;
        text-decoration: none;
        transition: all .18s cubic-bezier(.4,0,.2,1);
        white-space: nowrap;
        font-family: inherit;
        letter-spacing: -.01em;
    }
    .btn-primary {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
        color: #fff;
        box-shadow: 0 0 0 1px rgba(124,106,255,.25), 0 3px 12px rgba(124,106,255,.18);
    }
    .btn-primary:hover {
        box-shadow: 0 0 0 1px rgba(124,106,255,.45), 0 4px 20px rgba(124,106,255,.3);
        transform: translateY(-1px);
        filter: brightness(1.07);
        color: #fff;
    }
    .btn-ghost {
        background: transparent;
        color: var(--muted);
        border: 1px solid var(--border);
    }
    .btn-ghost:hover {
        color: var(--text2);
        border-color: var(--border2);
        background: rgba(255,255,255,.04);
    }
"""

_NAV_HTML = """
<nav>
  <a class="brand" href="{{ url_for('index') }}">
    <span class="brand-mark">M</span>
    <span class="brand-name">MediaIndex</span>
  </a>
  <div class="nav-sep"></div>
  <div class="nav-links">
    <a href="{{ url_for('index') }}"  class="{{ 'active' if request.path == '/' else '' }}">Gallery</a>
    <a href="{{ url_for('feed') }}"   class="{{ 'active' if request.path.startswith('/feed') else '' }}">Feed</a>
    <a href="{{ url_for('upload') }}" class="{{ 'active' if request.path.startswith('/upload') else '' }}">Upload</a>
    <a href="{{ url_for('tags') }}"   class="{{ 'active' if request.path.startswith('/tags') else '' }}">Tags</a>
  </div>
  <div class="nav-right">
    {% if g.user %}
      <div class="user-chip">
        <div class="user-avatar">{{ g.user.username[0].upper() }}</div>
        {{ g.user.username }}
      </div>
      <form method="post" action="{{ url_for('auth.logout') }}" style="display:inline;">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        <button type="submit" class="nav-logout" style="background:none;cursor:pointer;font-family:inherit;">Sign Out</button>
      </form>
    {% else %}
      <a class="btn btn-primary" href="{{ url_for('auth.login') }}" style="font-size:.8rem;padding:.3rem .75rem;">Sign In</a>
    {% endif %}
  </div>
</nav>
"""

_FLASH_HTML = """
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <div class="flashes">
      {% for cat, msg in messages %}
        <div class="flash flash-{{cat}}">
          <div class="flash-icon">
            {% if cat == 'success' %}✓{% elif cat == 'danger' %}✕{% else %}!{% endif %}
          </div>
          <span>{{msg}}</span>
        </div>
      {% endfor %}
    </div>
  {% endif %}
{% endwith %}
"""

# ---------------------------------------------------------------------------
#  Gallery / Index
# ---------------------------------------------------------------------------
TEMPLATE_INDEX = (
    """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>MediaIndex — Gallery</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="csrf-token" content="{{ csrf_token() }}"/>
  <style>"""
    + _COMMON_CSS
    + """
    /* ── TOOLBAR ─────────────────────────────────────────────────────────── */
    .toolbar {
        display: flex;
        gap: .5rem;
        flex-wrap: wrap;
        align-items: center;
        margin-bottom: 1.75rem;
        padding: .75rem 1rem;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--r);
    }

    .search-group {
        display: flex;
        gap: .4rem;
        flex: 1;
        min-width: 200px;
    }

    .input-wrap {
        position: relative;
        display: flex;
        align-items: center;
        flex: 1;
        min-width: 120px;
    }
    .input-icon {
        position: absolute;
        left: .7rem;
        color: var(--muted);
        pointer-events: none;
        display: flex;
        align-items: center;
    }
    .input-icon svg { width: 14px; height: 14px; }

    .toolbar input,
    .toolbar select {
        background: var(--surf2);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: .5rem .75rem;
        font-size: .845rem;
        font-family: inherit;
        width: 100%;
        transition: border-color .15s, box-shadow .15s, background .15s;
        letter-spacing: -.01em;
    }
    .input-wrap input { padding-left: 2.2rem; }
    .toolbar input:focus,
    .toolbar select:focus {
        outline: none;
        border-color: var(--border-hi);
        box-shadow: 0 0 0 3px rgba(124,106,255,.1);
        background: var(--surf3);
    }
    .toolbar select {
        min-width: 130px;
        cursor: pointer;
        appearance: none;
        -webkit-appearance: none;
        padding-right: 2rem;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2358687a'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right .7rem center;
    }
    .toolbar-actions { display: flex; gap: .4rem; }

    /* ── AI FILTER TOGGLE ────────────────────────────────────────────────── */
    .ai-toggle {
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        cursor: pointer;
        user-select: none;
        padding: .48rem .75rem;
        border-radius: 8px;
        border: 1px solid var(--border);
        background: var(--surf2);
        font-size: .845rem;
        color: var(--muted);
        transition: all .15s;
        white-space: nowrap;
        flex-shrink: 0;
    }
    .ai-toggle:hover { border-color: var(--border2); color: var(--text2); }
    .ai-toggle input { display: none; }
    .ai-toggle-track {
        width: 28px; height: 16px;
        border-radius: 99px;
        background: var(--surf3);
        border: 1px solid var(--border2);
        position: relative;
        flex-shrink: 0;
        transition: background .15s, border-color .15s;
    }
    .ai-toggle-track::after {
        content: '';
        position: absolute;
        width: 10px; height: 10px;
        border-radius: 50%;
        background: var(--muted);
        top: 50%; left: 2px;
        transform: translateY(-50%);
        transition: left .15s, background .15s;
    }
    .ai-toggle input:checked ~ .ai-toggle-track {
        background: rgba(248,81,73,.2);
        border-color: rgba(248,81,73,.45);
    }
    .ai-toggle input:checked ~ .ai-toggle-track::after {
        left: 14px;
        background: var(--danger);
    }
    .ai-toggle:has(input:checked) {
        border-color: rgba(248,81,73,.3);
        background: rgba(248,81,73,.06);
        color: var(--danger);
    }

    /* ── COUNT BAR ───────────────────────────────────────────────────────── */
    .count-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .count-label {
        font-size: .8rem;
        color: var(--muted);
        letter-spacing: -.01em;
    }

    /* ── GALLERY ─────────────────────────────────────────────────────────── */
    .gallery {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
        gap: 1rem;
    }

    .gallery-item {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--r);
        overflow: hidden;
        position: relative;
        cursor: pointer;
        transition: border-color .2s, transform .22s cubic-bezier(.4,0,.2,1), box-shadow .22s;
        group: '';
    }
    .gallery-item:hover {
        border-color: rgba(124,106,255,.45);
        transform: translateY(-3px);
        box-shadow:
            0 16px 40px rgba(0,0,0,.55),
            0 0 0 1px rgba(124,106,255,.2),
            0 0 30px rgba(124,106,255,.08);
    }

    .thumb-wrapper {
        aspect-ratio: 1;
        overflow: hidden;
        background: var(--surf2);
        position: relative;
    }
    .thumb {
        width: 100%; height: 100%;
        object-fit: cover;
        display: block;
        transition: transform .35s cubic-bezier(.4,0,.2,1);
    }
    .gallery-item:hover .thumb { transform: scale(1.05); }

    /* Type badge */
    .type-badge {
        position: absolute;
        bottom: .45rem; left: .45rem;
        padding: .15em .5em;
        border-radius: 4px;
        font-size: .68rem;
        font-weight: 700;
        letter-spacing: .04em;
        text-transform: uppercase;
        pointer-events: none;
        opacity: 0;
        transform: translateY(3px);
        transition: opacity .2s, transform .2s;
        backdrop-filter: blur(6px);
    }
    .gallery-item:hover .type-badge { opacity: 1; transform: translateY(0); }
    .type-badge.video { background: rgba(92,124,255,.7); color: #c0cfff; border: 1px solid rgba(92,124,255,.3); }
    .type-badge.gif   { background: rgba(168,85,247,.7); color: #e8c5ff; border: 1px solid rgba(168,85,247,.3); }
    .type-badge.image  { background: rgba(20,160,120,.7); color: #a0f0d8; border: 1px solid rgba(20,160,120,.3); }

    /* Hover gradient overlay */
    .thumb-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(2,4,8,.7) 0%, transparent 50%);
        opacity: 0;
        transition: opacity .2s;
        pointer-events: none;
    }
    .gallery-item:hover .thumb-overlay { opacity: 1; }

    /* Card body */
    .card-body {
        padding: .6rem .7rem .7rem;
    }
    .card-tags {
        display: flex;
        flex-wrap: wrap;
        gap: .25rem;
        min-height: 1.5rem;
    }

    /* Tag pills */
    .tag-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(124,106,255,.1);
        color: rgba(150,130,255,.9);
        border: 1px solid rgba(124,106,255,.18);
        border-radius: 4px;
        padding: .08em .45em;
        font-size: .68rem;
        font-weight: 500;
        letter-spacing: -.005em;
        transition: background .15s, border-color .15s;
    }
    .tag-pill:hover { background: rgba(124,106,255,.18); border-color: rgba(124,106,255,.35); }
    .tag-pill.user-tag {
        background: rgba(210,153,34,.1);
        color: rgba(240,190,60,.9);
        border-color: rgba(210,153,34,.2);
    }
    .tag-pill.type-tag {
        background: rgba(63,185,80,.09);
        color: rgba(80,210,100,.9);
        border-color: rgba(63,185,80,.2);
    }
    .no-tags {
        font-size: .72rem;
        color: var(--muted);
        font-style: italic;
    }

    /* ── ACTION BUTTONS ──────────────────────────────────────────────────── */
    .action-buttons {
        position: absolute;
        top: .5rem; right: .5rem;
        display: flex;
        gap: .3rem;
        opacity: 0;
        transform: translateY(-4px);
        transition: opacity .18s, transform .18s;
    }
    .gallery-item:hover .action-buttons {
        opacity: 1;
        transform: translateY(0);
    }
    .action-btn {
        width: 30px; height: 30px;
        border-radius: 7px;
        border: none;
        cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        font-size: .85rem;
        transition: all .15s;
        backdrop-filter: blur(8px);
    }
    .edit-btn {
        background: rgba(8,10,18,.75);
        color: #93c5fd;
        border: 1px solid rgba(147,197,253,.15);
    }
    .edit-btn:hover { background: rgba(99,102,241,.8); color: #fff; border-color: transparent; }
    .delete-btn {
        background: rgba(8,10,18,.75);
        color: #fca5a5;
        border: 1px solid rgba(252,165,165,.15);
    }
    .delete-btn:hover { background: rgba(220,38,38,.8); color: #fff; border-color: transparent; }

    /* ── EDIT FORM ───────────────────────────────────────────────────────── */
    .edit-form {
        display: none;
        position: absolute;
        bottom: 0; left: 0; right: 0;
        background: rgba(6,10,18,.97);
        padding: .65rem .7rem;
        border-top: 1px solid var(--border);
        backdrop-filter: blur(10px);
    }
    .edit-form.active { display: block; }
    .edit-form input {
        width: 100%;
        background: var(--surf2);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: .38rem .55rem;
        font-size: .8rem;
        font-family: inherit;
        margin-bottom: .38rem;
        transition: border-color .15s;
    }
    .edit-form input:focus { outline: none; border-color: var(--border-hi); }
    .edit-form-btns { display: flex; gap: .3rem; justify-content: flex-end; }
    .edit-form button {
        padding: .27rem .65rem;
        border-radius: 6px;
        border: none;
        font-size: .77rem;
        cursor: pointer;
        font-weight: 600;
        font-family: inherit;
        transition: all .15s;
    }
    .save-btn   { background: var(--accent); color: #fff; }
    .save-btn:hover { background: var(--accent2); }
    .cancel-btn { background: var(--surf3); color: var(--muted); border: 1px solid var(--border); }
    .cancel-btn:hover { color: var(--text); }

    /* ── MODAL ───────────────────────────────────────────────────────────── */
    .modal-bg {
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,.82);
        backdrop-filter: blur(10px) saturate(140%);
        -webkit-backdrop-filter: blur(10px) saturate(140%);
        align-items: center;
        justify-content: center;
        z-index: 200;
        padding: 1.25rem;
        animation: none;
    }
    .modal-bg.active {
        display: flex;
        animation: modalBgIn .22s ease;
    }
    @keyframes modalBgIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    .modal-box {
        background: var(--surface);
        border: 1px solid var(--border2);
        border-radius: 16px;
        width: min(92vw, 1000px);
        max-height: 90vh;
        overflow: hidden;
        position: relative;
        box-shadow: 0 32px 80px rgba(0,0,0,.8), 0 0 0 1px rgba(255,255,255,.06);
        animation: modalBoxIn .22s cubic-bezier(.4,0,.2,1);
        display: flex;
        flex-direction: column;
    }
    @keyframes modalBoxIn {
        from { opacity: 0; transform: scale(.96) translateY(8px); }
        to   { opacity: 1; transform: scale(1) translateY(0); }
    }
    .modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: .75rem 1rem;
        border-bottom: 1px solid var(--border);
        flex-shrink: 0;
    }
    .modal-title {
        font-size: .8rem;
        font-weight: 600;
        color: var(--muted);
        letter-spacing: .04em;
        text-transform: uppercase;
    }
    .modal-header-actions { display: flex; gap: .4rem; }
    .modal-btn {
        display: inline-flex;
        align-items: center;
        gap: .3rem;
        background: var(--surf2);
        border: 1px solid var(--border);
        border-radius: 7px;
        padding: .3rem .65rem;
        font-size: .8rem;
        color: var(--muted);
        cursor: pointer;
        text-decoration: none;
        transition: all .15s;
        font-family: inherit;
    }
    .modal-btn:hover { color: var(--text); border-color: var(--border2); background: var(--surf3); }
    .modal-close {
        width: 28px; height: 28px; padding: 0;
        background: var(--surf2);
        border: 1px solid var(--border);
        border-radius: 7px;
        color: var(--muted);
        cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        font-size: .9rem;
        transition: all .15s;
        font-family: inherit;
    }
    .modal-close:hover { background: rgba(248,81,73,.15); border-color: rgba(248,81,73,.3); color: var(--danger); }
    .modal-body {
        overflow: auto;
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(0,0,0,.25);
        padding: 1rem;
        min-height: 0;
    }
    .modal-media {
        max-width: 100%;
        max-height: 72vh;
        display: block;
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,.6);
    }
    .modal-footer {
        padding: .65rem 1rem;
        border-top: 1px solid var(--border);
        flex-shrink: 0;
    }
    .modal-tags {
        display: flex;
        flex-wrap: wrap;
        gap: .25rem;
        font-size: .8rem;
    }
    .modal-tag-label {
        color: var(--muted);
        margin-right: .25rem;
        font-size: .78rem;
    }

    /* ── MISC ────────────────────────────────────────────────────────────── */
    #scroll-sentinel {
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--muted);
        font-size: .82rem;
        grid-column: 1 / -1;
    }

    .empty {
        grid-column: 1 / -1;
        text-align: center;
        padding: 6em 2em;
        color: var(--muted);
    }
    .empty-icon {
        font-size: 3.5rem;
        opacity: .18;
        margin-bottom: .75rem;
        line-height: 1;
    }
    .empty h3 { font-size: 1rem; font-weight: 500; color: var(--text2); margin-bottom: .35rem; }
    .empty p  { font-size: .85rem; }

    /* Loader ring */
    .loader {
        width: 20px; height: 20px;
        border: 2px solid var(--border2);
        border-top-color: var(--accent);
        border-radius: 50%;
        animation: spin .65s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    @media (max-width: 680px) {
        nav { padding: 0 1rem; gap: .5rem; }
        .nav-links a { padding: .35rem .55rem; font-size: .78rem; }
        .brand-name { display: none; }
        .container { padding: 1rem; }
        .toolbar { padding: .6rem .75rem; }
        .search-group { flex-wrap: wrap; }
        .gallery { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: .6rem; }
    }
  </style>

  <script>
    /* ── Lazy image observer ── */
    const lazyObserver = new IntersectionObserver((entries, obs) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.src = e.target.dataset.src;
                obs.unobserve(e.target);
            }
        });
    }, { rootMargin: '150px', threshold: 0.05 });

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('img.thumb').forEach(img => lazyObserver.observe(img));

        fetch('/api/tags').then(r => r.json()).then(tags => {
            const dl = document.getElementById('tag-suggestions');
            tags.forEach(t => {
                const o = document.createElement('option');
                o.value = t;
                dl.appendChild(o);
            });
        }).catch(() => {});

        const sentinel = document.getElementById('scroll-sentinel');
        const gallery  = document.querySelector('.gallery');
        if (!sentinel || !gallery) return;

        let page = 1, loading = false, exhausted = false;
        const params = new URLSearchParams(window.location.search);

        function esc(s) {
            return (s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;')
                           .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
        }

        function getType(tags) {
            if (!tags) return '';
            const t = tags.split(',').map(x => x.trim());
            if (t.includes('video')) return 'video';
            if (t.includes('gif'))   return 'gif';
            if (t.includes('image'))  return 'image';
            return '';
        }

        function makePills(tagsStr) {
            if (!tagsStr) return '<span class="no-tags">No tags</span>';
            return tagsStr.split(',').filter(t => t.trim()).map(t => {
                const tag = t.trim();
                let cls = 'tag-pill';
                if (tag.startsWith('user:')) cls += ' user-tag';
                else if (['image','gif','video'].includes(tag)) cls += ' type-tag';
                return `<span class="${cls}">${esc(tag)}</span>`;
            }).join('');
        }

        function createCard(media) {
            const id   = media.id;
            const type = media.type || getType(media.tags);
            const div  = document.createElement('div');
            div.className = 'gallery-item';
            div.innerHTML =
                `<div class="action-buttons">
                   <button class="action-btn edit-btn" onclick="event.stopPropagation();showEditForm(${id})" title="Edit Tags">✎</button>
                   <button class="action-btn delete-btn" onclick="event.stopPropagation();deleteMedia(${id})" title="Delete File">×</button>
                 </div>
                 <div class="thumb-wrapper">
                   <img class="thumb" onclick="openModal(${id})"
                        data-src="/thumbs/${esc(media.thumb)}"
                        src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
                        alt=""/>
                   <div class="thumb-overlay"></div>
                   ${type ? `<span class="type-badge ${esc(type)}">${esc(type)}</span>` : ''}
                 </div>
                 <div class="card-body">
                   <div class="card-tags">${makePills(media.tags)}</div>
                 </div>
                 <div id="edit-form-${id}" class="edit-form">
                   <input type="text" id="edit-input-${id}" value="${esc(media.tags||'')}" placeholder="Tags separated by commas…" list="tag-suggestions">
                   <div class="edit-form-btns">
                     <button class="cancel-btn" onclick="hideEditForm(${id})">Cancel</button>
                     <button class="save-btn" onclick="saveEditedTags(${id})">Save</button>
                   </div>
                 </div>`;
            return div;
        }

        function loadNextPage() {
            if (loading || exhausted) return;
            loading = true;
            sentinel.innerHTML = '<div class="loader"></div>';
            page++;
            const url = new URL('/api/media', location.origin);
            ['type','search','exclude_tags','hide_ai'].forEach(k => {
                const v = params.get(k);
                if (v) url.searchParams.set(k, v);
            });
            url.searchParams.set('page', page);
            fetch(url).then(r => r.json()).then(data => {
                data.media.forEach(m => {
                    const card = createCard(m);
                    gallery.insertBefore(card, sentinel);
                    lazyObserver.observe(card.querySelector('img.thumb'));
                });
                sentinel.innerHTML = '';
                if (!data.has_more) {
                    exhausted = true;
                    sentinel.style.display = 'none';
                    scrollObs.disconnect();
                }
                loading = false;
            }).catch(() => { loading = false; sentinel.innerHTML = ''; });
        }

        const scrollObs = new IntersectionObserver(
            entries => { if (entries[0].isIntersecting) loadNextPage(); },
            { rootMargin: '250px' }
        );
        scrollObs.observe(sentinel);
    });

    const csrfToken = () => document.querySelector('meta[name="csrf-token"]').content;

    /* ── Modal ── */
    function openModal(id) {
        fetch('/mediadata/' + id).then(r => r.json()).then(d => {
            const modal    = document.getElementById('modal-bg');
            const filename = d.filepath.split('/').pop();
            const isVideo  = d.type === 'video';
            const container = modal.querySelector('.modal-view-content');
            container.innerHTML = '';
            const el = document.createElement(isVideo ? 'video' : 'img');
            el.className = 'modal-media';
            el.src = '/media/' + filename;
            if (isVideo) el.controls = true;
            else el.alt = '';
            container.appendChild(el);

            /* Tags in footer */
            const footer = modal.querySelector('.modal-tags');
            if (d.tags) {
                footer.innerHTML = '<span class="modal-tag-label">Tags:</span>' +
                    d.tags.split(',').filter(t => t.trim()).map(t => {
                        const tag = t.trim();
                        let cls = 'tag-pill';
                        if (tag.startsWith('user:')) cls += ' user-tag';
                        else if (['image','gif','video'].includes(tag)) cls += ' type-tag';
                        const e = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                        return `<span class="${cls}">${e(tag)}</span>`;
                    }).join('');
            } else {
                footer.innerHTML = '<span class="no-tags">No tags</span>';
            }

            const dl = document.getElementById('modal-download');
            dl.href = '/media/' + filename;
            dl.setAttribute('download', filename);
            dl.textContent = '↓ ' + filename;

            modal.dataset.currentId = id;
            modal.classList.add('active');
        });
    }

    function closeModal() {
        const modal = document.getElementById('modal-bg');
        modal.classList.remove('active');
        // Stop video playback
        const v = modal.querySelector('video');
        if (v) { v.pause(); v.src = ''; }
        modal.querySelector('.modal-view-content').innerHTML = '';
        modal.querySelector('.modal-tags').innerHTML = '';
    }

    function modalDelete() {
        const id = document.getElementById('modal-bg').dataset.currentId;
        if (!id || !confirm('Are you sure you want to delete this file?')) return;
        fetch(`/delete/${id}`, { method: 'POST', headers: {'X-CSRFToken': csrfToken()} })
            .then(r => { if (r.ok) location.reload(); else alert('Error deleting file.'); })
            .catch(() => alert('Error deleting file.'));
    }

    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') closeModal();
    });

    function showEditForm(id) {
        document.querySelectorAll('.edit-form').forEach(f => f.classList.remove('active'));
        document.getElementById('edit-form-' + id).classList.add('active');
    }
    function hideEditForm(id) {
        document.getElementById('edit-form-' + id).classList.remove('active');
    }
    function saveEditedTags(id) {
        const input = document.getElementById('edit-input-' + id);
        const fd = new FormData();
        fd.append('tags', input.value.trim());
        fetch(`/edit/${id}`, { method: 'POST', headers: {'X-CSRFToken': csrfToken()}, body: fd })
            .then(r => { if (r.ok) location.reload(); else alert('Error saving.'); })
            .catch(() => alert('Error saving.'));
    }
    function deleteMedia(id) {
        if (!confirm('Are you sure you want to delete this file?')) return;
        fetch(`/delete/${id}`, { method: 'POST', headers: {'X-CSRFToken': csrfToken()} })
            .then(r => { if (r.ok) location.reload(); else alert('Error deleting file.'); })
            .catch(() => alert('Error deleting file.'));
    }
  </script>
</head>
<body>
"""
    + _NAV_HTML
    + """
<div class="container">
"""
    + _FLASH_HTML
    + """
  <form class="toolbar" action="{{ url_for('index') }}" method="get" autocomplete="off">
    <div class="search-group">
      <div class="input-wrap">
        <span class="input-icon">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="6.5" cy="6.5" r="4.5"/><path d="M10.5 10.5l3 3"/>
          </svg>
        </span>
        <input name="search" type="text" placeholder="Search tags…" value="{{ search|e }}">
      </div>
      <div class="input-wrap">
        <span class="input-icon">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M12 4L4 12M4 4l8 8"/>
          </svg>
        </span>
        <input name="exclude_tags" type="text" placeholder="Exclude tags…" value="{{ exclude_tags|e }}">
      </div>
    </div>
    <select name="type">
      <option value="all"   {% if filter_type=='all'   %}selected{% endif %}>All types</option>
      <option value="image"  {% if filter_type=='image'  %}selected{% endif %}>Images</option>
      <option value="video" {% if filter_type=='video' %}selected{% endif %}>Videos</option>
      <option value="gif"   {% if filter_type=='gif'   %}selected{% endif %}>GIFs</option>
    </select>
    <label class="ai-toggle" title="Hide content with the following tags: fake, ai, grok, gemini, chatgpt">
      <input type="checkbox" name="hide_ai" value="1" {% if hide_ai == '1' %}checked{% endif %} onchange="this.form.submit()">
      <span class="ai-toggle-track"></span>
      <span>Hide AI content</span>
    </label>
    <div class="toolbar-actions">
      <button class="btn btn-primary" type="submit">Search</button>
      <a class="btn btn-ghost" href="{{ url_for('index') }}">Reset</a>
    </div>
  </form>

  <div class="gallery">
    {% for media in media %}
      {%- set ext = media[1].rsplit('.',1)[-1].lower() -%}
      {%- set mtype = 'video' if ext in ['mp4','webm','avi','mov','mkv'] else ('gif' if ext == 'gif' else 'image') -%}
      <div class="gallery-item">
        <div class="action-buttons">
          <button class="action-btn edit-btn"   onclick="event.stopPropagation(); showEditForm({{ media[0] }})" title="Edit tags">✎</button>
          <button class="action-btn delete-btn" onclick="event.stopPropagation(); deleteMedia({{ media[0] }})"  title="Delete File">×</button>
        </div>
        <div class="thumb-wrapper">
          <img class="thumb" loading="lazy" onclick="openModal({{ media[0] }})"
               data-src="/thumbs/{{ media[2].split('/')[-1] }}"
               src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
               alt=""/>
          <div class="thumb-overlay"></div>
          <span class="type-badge {{ mtype }}">{{ mtype }}</span>
        </div>
        <div class="card-body">
          <div class="card-tags">
            {% if media[3] %}
              {% for tag in media[3].split(',') %}{% if tag.strip() %}
                <span class="tag-pill {% if tag.strip().startswith('user:') %}user-tag{% elif tag.strip() in ['image','gif','video'] %}type-tag{% endif %}">{{ tag.strip() }}</span>
              {% endif %}{% endfor %}
            {% else %}
              <span class="no-tags">No Tags</span>
            {% endif %}
          </div>
        </div>
        <div id="edit-form-{{ media[0] }}" class="edit-form">
          <input type="text" id="edit-input-{{ media[0] }}" value="{{ media[3] or '' }}" placeholder="Tags separated by commas…" list="tag-suggestions">
          <div class="edit-form-btns">
            <button type="button" class="cancel-btn" onclick="hideEditForm({{ media[0] }})">Cancel</button>
            <button type="button" class="save-btn"   onclick="saveEditedTags({{ media[0] }})">Save</button>
          </div>
        </div>
      </div>
    {% endfor %}

    {% if not media %}
      <div class="empty">
        <div class="empty-icon">&#128193;</div>
        <h3>No entries found</h3>
        <p>Try different search terms or reset the filter.</p>
      </div>
    {% endif %}

    <div id="scroll-sentinel"></div>
  </div>
</div>

<datalist id="tag-suggestions"></datalist>

<!-- ── MODAL ── -->
<div id="modal-bg" class="modal-bg" onclick="if(event.target===this) closeModal()">
  <div class="modal-box" onclick="event.stopPropagation()">
    <div class="modal-header">
      <span class="modal-title">Preview</span>
      <div class="modal-header-actions">
        <a id="modal-download" href="#" download class="modal-btn">↓ Download</a>
        <button class="modal-btn modal-delete-btn" onclick="modalDelete()" title="Delete file" style="color:var(--danger);border-color:rgba(248,81,73,.25);">🗑 Delete</button>
        <button class="modal-close" onclick="closeModal()" title="Close">×</button>
      </div>
    </div>
    <div class="modal-body">
      <div class="modal-view-content"></div>
    </div>
    <div class="modal-footer">
      <div class="modal-tags"></div>
    </div>
  </div>
</div>

</body>
</html>"""
)

# ---------------------------------------------------------------------------
#  Upload
# ---------------------------------------------------------------------------
TEMPLATE_UPLOAD = (
    """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>MediaIndex — Upload</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="csrf-token" content="{{ csrf_token() }}"/>
  <style>"""
    + _COMMON_CSS
    + """
    /* ── UPLOAD PAGE ─────────────────────────────────────────────────────── */
    .page-header { margin-bottom: 1.75rem; }
    .page-title  {
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: -.03em;
        color: var(--text);
        margin-bottom: .25rem;
    }
    .page-sub { font-size: .85rem; color: var(--muted); }

    .upload-layout {
        display: grid;
        grid-template-columns: 1fr 320px;
        gap: 1.25rem;
        align-items: start;
    }

    .upload-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.5rem;
    }

    /* Drop zone */
    .drop-zone {
        position: relative;
        border: 2px dashed var(--border2);
        border-radius: 10px;
        padding: 4em 2em;
        text-align: center;
        cursor: pointer;
        transition: border-color .2s, background .2s;
        margin-bottom: 1.25rem;
        overflow: hidden;
    }
    .drop-zone::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse 60% 60% at 50% 50%, rgba(124,106,255,.05), transparent);
        opacity: 0;
        transition: opacity .3s;
        pointer-events: none;
    }
    .drop-zone:hover::before,
    .drop-zone.drag-over::before { opacity: 1; }
    .drop-zone:hover,
    .drop-zone.drag-over {
        border-color: rgba(124,106,255,.6);
        background: rgba(124,106,255,.03);
    }
    .drop-zone.drag-over {
        border-color: var(--accent);
        animation: pulseBorder 1s ease-in-out infinite alternate;
    }
    @keyframes pulseBorder {
        from { border-color: rgba(124,106,255,.5); }
        to   { border-color: rgba(124,106,255,1); }
    }
    .drop-zone-icon {
        font-size: 3rem;
        line-height: 1;
        margin-bottom: .75rem;
        opacity: .25;
        display: block;
    }
    .drop-zone h3 {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: .4rem;
        color: var(--text);
        letter-spacing: -.02em;
    }
    .drop-zone p {
        color: var(--muted);
        font-size: .845rem;
        margin: 0;
    }
    .drop-zone em {
        color: var(--accent);
        font-style: normal;
        cursor: pointer;
        font-weight: 500;
        text-decoration: underline;
        text-decoration-style: dotted;
        text-underline-offset: 2px;
    }
    .drop-zone em:hover { color: #a89bff; }

    #filesInput { display: none; }

    /* Preview list */
    #previews { margin-top: .25rem; display: flex; flex-direction: column; gap: .65rem; }

    .preview-item {
        background: var(--surf2);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: .85rem 1rem;
        display: flex;
        gap: .9rem;
        align-items: flex-start;
        transition: border-color .15s;
    }
    .preview-item:hover { border-color: var(--border2); }

    .preview-thumb {
        width: 80px; height: 60px;
        object-fit: cover;
        border-radius: 7px;
        background: var(--surf3);
        flex-shrink: 0;
        border: 1px solid var(--border);
    }

    .preview-details { flex: 1; min-width: 0; }
    .preview-filename {
        font-size: .78rem;
        color: var(--text2);
        font-weight: 500;
        margin-bottom: .5rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        letter-spacing: -.01em;
    }
    .preview-details input {
        width: 100%;
        background: var(--surf3);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 7px;
        padding: .42rem .65rem;
        font-size: .845rem;
        font-family: inherit;
        transition: border-color .15s, box-shadow .15s;
    }
    .preview-details input:focus {
        outline: none;
        border-color: var(--border-hi);
        box-shadow: 0 0 0 3px rgba(124,106,255,.1);
    }

    .upload-btn {
        width: 100%;
        padding: .75rem;
        margin-top: 1rem;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
        color: #fff;
        border: none;
        border-radius: 9px;
        font-size: .95rem;
        font-weight: 600;
        cursor: pointer;
        font-family: inherit;
        letter-spacing: -.01em;
        box-shadow: 0 0 0 1px rgba(124,106,255,.25), 0 4px 16px rgba(124,106,255,.2);
        transition: all .18s;
    }
    .upload-btn:hover {
        filter: brightness(1.08);
        box-shadow: 0 0 0 1px rgba(124,106,255,.45), 0 6px 24px rgba(124,106,255,.3);
        transform: translateY(-1px);
    }
    .upload-btn:active { transform: translateY(0); filter: brightness(.96); }

    /* Sidebar info */
    .info-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.25rem;
        font-size: .845rem;
        color: var(--text2);
        line-height: 1.75;
    }
    .info-card-title {
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .06em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: .85rem;
        display: flex;
        align-items: center;
        gap: .4rem;
    }
    .info-card-title::before {
        content: '';
        display: block;
        width: 3px; height: 14px;
        background: linear-gradient(to bottom, var(--accent), #a855f7);
        border-radius: 99px;
    }
    .info-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        padding: .4rem 0;
        border-bottom: 1px solid var(--border);
        gap: .5rem;
    }
    .info-row:last-child { border-bottom: none; }
    .info-key {
        color: var(--muted);
        font-size: .78rem;
        font-weight: 500;
        flex-shrink: 0;
    }
    .info-val {
        color: var(--text2);
        font-size: .8rem;
        text-align: right;
        font-feature-settings: 'tnum';
    }
    .format-chips {
        display: flex;
        flex-wrap: wrap;
        gap: .25rem;
        justify-content: flex-end;
    }
    .format-chip {
        padding: .1em .45em;
        background: var(--surf2);
        border: 1px solid var(--border);
        border-radius: 4px;
        font-size: .7rem;
        color: var(--muted);
        font-feature-settings: 'tnum';
    }

    @media (max-width: 820px) {
        .upload-layout { grid-template-columns: 1fr; }
    }
    @media (max-width: 680px) {
        nav { padding: 0 1rem; }
        .brand-name { display: none; }
        .container { padding: 1rem; }
        .preview-item { flex-direction: column; }
        .preview-thumb { width: 100%; height: 140px; }
    }
  </style>
</head>
<body>
"""
    + _NAV_HTML
    + """
<div class="container">
"""
    + _FLASH_HTML
    + """
  <div class="page-header">
    <div class="page-title">Upload</div>
    <div class="page-sub">Upload images, GIFs, and videos</div>
  </div>

  <div class="upload-layout">
    <div class="upload-card">
      <form id="uploadForm" method="POST" enctype="multipart/form-data">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        <input id="filesInput" type="file" name="files" multiple
               accept="image/*,video/*,.webp,.heic,.gif">

        <div class="drop-zone" id="dropZone">
          <span class="drop-zone-icon">&#8659;</span>
          <h3>Drag files here</h3>
          <p>or <em onclick="document.getElementById('filesInput').click()">Select files</em></p>
        </div>

        <div id="previews"></div>

        <button class="upload-btn" type="submit">Start upload</button>
      </form>
    </div>

    <div class="info-card">
      <div class="info-card-title">Information</div>
      <div class="info-row">
        <span class="info-key">Images</span>
        <div class="info-val">
          <div class="format-chips">
            <span class="format-chip">jpg</span>
            <span class="format-chip">png</span>
            <span class="format-chip">webp</span>
            <span class="format-chip">heic</span>
          </div>
        </div>
      </div>
      <div class="info-row">
        <span class="info-key">GIF</span>
        <div class="info-val"><div class="format-chips"><span class="format-chip">gif</span></div></div>
      </div>
      <div class="info-row">
        <span class="info-key">Videos</span>
        <div class="info-val">
          <div class="format-chips">
            <span class="format-chip">mp4</span>
            <span class="format-chip">webm</span>
            <span class="format-chip">avi</span>
            <span class="format-chip">mov</span>
            <span class="format-chip">mkv</span>
          </div>
        </div>
      </div>
      <div class="info-row">
        <span class="info-key">Max. Size</span>
        <span class="info-val">10 GiB</span>
      </div>
      <div class="info-row">
        <span class="info-key">Duplicates</span>
        <span class="info-val">will be skipped</span>
      </div>
      <div class="info-row">
        <span class="info-key">Tags</span>
        <span class="info-val">comma-separated</span>
      </div>
    </div>
  </div>
</div>

<datalist id="tag-suggestions"></datalist>
<script>
document.addEventListener('DOMContentLoaded', () => {
    const filesInput  = document.getElementById('filesInput');
    const previewsDiv = document.getElementById('previews');
    const dropZone    = document.getElementById('dropZone');

    fetch('/api/tags').then(r => r.json()).then(tags => {
        const dl = document.getElementById('tag-suggestions');
        tags.forEach(t => { const o = document.createElement('option'); o.value = t; dl.appendChild(o); });
    }).catch(() => {});

    dropZone.addEventListener('click', e => {
        if (e.target.tagName !== 'EM') filesInput.click();
    });
    dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', e => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        filesInput.files = e.dataTransfer.files;
        filesInput.dispatchEvent(new Event('change'));
    });

    filesInput.addEventListener('change', event => {
        const files = event.target.files;
        previewsDiv.innerHTML = '';
        if (!files.length) return;

        Array.from(files).forEach((file, i) => {
            const div = document.createElement('div');
            div.className = 'preview-item';

            const url = URL.createObjectURL(file);
            let media;
            if (file.type.startsWith('image/')) {
                media = document.createElement('img');
                media.src = url;
                media.addEventListener('load', () => URL.revokeObjectURL(url), { once: true });
            } else if (file.type.startsWith('video/')) {
                media = document.createElement('video');
                media.src = url;
                media.addEventListener('loadeddata', () => URL.revokeObjectURL(url), { once: true });
            } else {
                media = document.createElement('div');
                media.textContent = file.name.split('.').pop().toUpperCase();
                media.style.cssText =
                    'width:80px;height:60px;display:flex;align-items:center;justify-content:center;' +
                    'background:var(--surf3);border-radius:7px;font-size:.7rem;font-weight:700;' +
                    'color:var(--muted);letter-spacing:.04em;';
            }
            media.className = 'preview-thumb';

            const details  = document.createElement('div');
            details.className = 'preview-details';
            const fname    = document.createElement('div');
            fname.className = 'preview-filename';
            fname.textContent = file.name;
            const tagInput = document.createElement('input');
            tagInput.type = 'text';
            tagInput.name = 'tags_' + i;
            tagInput.placeholder = 'Tags (separated by commas)…';
            tagInput.setAttribute('list', 'tag-suggestions');

            details.appendChild(fname);
            details.appendChild(tagInput);
            div.appendChild(media);
            div.appendChild(details);
            previewsDiv.appendChild(div);
        });
    });
});
</script>
</body>
</html>"""
)

# ---------------------------------------------------------------------------
#  Tags
# ---------------------------------------------------------------------------
TEMPLATE_TAGS = (
    """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>MediaIndex — Tags</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="csrf-token" content="{{ csrf_token() }}"/>
  <style>"""
    + _COMMON_CSS
    + """
    /* ── TAGS PAGE ───────────────────────────────────────────────────────── */
    .page-header {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 1.75rem;
        flex-wrap: wrap;
    }
    .page-title-group {}
    .page-title { font-size: 1.35rem; font-weight: 700; letter-spacing: -.03em; }
    .page-sub   { font-size: .845rem; color: var(--muted); margin-top: .2rem; }

    /* Stats row */
    .stats-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: .85rem;
        margin-bottom: 1.75rem;
    }
    .stat-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        position: relative;
        overflow: hidden;
        transition: border-color .15s;
    }
    .stat-card:hover { border-color: var(--border2); }
    .stat-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), #a855f7);
        opacity: .7;
    }
    .stat-num {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -.04em;
        background: linear-gradient(135deg, var(--text) 0%, var(--text2) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        margin-bottom: .25rem;
    }
    .stat-label { font-size: .78rem; color: var(--muted); font-weight: 500; letter-spacing: .01em; }

    /* Search */
    .tag-toolbar {
        display: flex;
        align-items: center;
        gap: .75rem;
        margin-bottom: 1.25rem;
        max-width: 460px;
    }
    .tag-search-wrap {
        position: relative;
        flex: 1;
    }
    .tag-search-wrap .s-icon {
        position: absolute;
        left: .7rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--muted);
        display: flex;
        pointer-events: none;
    }
    .tag-search-wrap .s-icon svg { width: 14px; height: 14px; }
    #tagSearch {
        width: 100%;
        background: var(--surface);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: .5rem .75rem .5rem 2.25rem;
        font-size: .845rem;
        font-family: inherit;
        transition: border-color .15s, box-shadow .15s;
    }
    #tagSearch:focus {
        outline: none;
        border-color: var(--border-hi);
        box-shadow: 0 0 0 3px rgba(124,106,255,.1);
    }
    #tagCount {
        font-size: .78rem;
        color: var(--muted);
        white-space: nowrap;
        flex-shrink: 0;
    }

    /* Tag list */
    .tag-list { display: flex; flex-direction: column; gap: .35rem; }

    .tag-item {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 9px;
        padding: .6rem 1rem;
        display: flex;
        align-items: center;
        gap: .75rem;
        cursor: pointer;
        transition: border-color .15s, background .15s, transform .15s;
        text-decoration: none;
    }
    .tag-item:hover {
        border-color: rgba(124,106,255,.35);
        background: rgba(124,106,255,.03);
        transform: translateX(3px);
    }

    .tag-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
        background: var(--muted);
    }
    .tag-dot.is-user  { background: var(--warning); box-shadow: 0 0 6px rgba(210,153,34,.5); }
    .tag-dot.is-type  { background: var(--success); box-shadow: 0 0 6px rgba(63,185,80,.5);  }
    .tag-dot.is-other { background: var(--accent);  box-shadow: 0 0 6px rgba(124,106,255,.4); }

    .tag-name {
        font-size: .875rem;
        font-weight: 500;
        min-width: 0;
        flex-shrink: 0;
        max-width: 280px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        letter-spacing: -.01em;
        color: var(--text);
    }
    .tag-name.is-user { color: var(--warning); }
    .tag-name.is-type { color: var(--success); }

    .tag-bar-track {
        flex: 1;
        height: 3px;
        background: var(--surf2);
        border-radius: 99px;
        overflow: hidden;
    }
    .tag-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--accent), #a855f7);
        border-radius: 99px;
        transition: width .4s cubic-bezier(.4,0,.2,1);
    }
    .tag-count {
        background: var(--surf2);
        color: var(--muted);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: .15em .7em;
        font-size: .75rem;
        font-weight: 600;
        flex-shrink: 0;
        font-feature-settings: 'tnum';
        letter-spacing: -.01em;
        min-width: 2rem;
        text-align: center;
    }

    /* Empty state */
    .no-tags-msg {
        text-align: center;
        padding: 5em 2em;
        color: var(--muted);
    }
    .no-tags-msg .empty-icon { font-size: 3rem; opacity: .2; margin-bottom: .75rem; }
    .no-tags-msg p { margin-top: .5em; font-size: .875rem; }
    .no-tags-msg p:first-of-type { font-size: 1rem; font-weight: 500; color: var(--text2); }

    @media (max-width: 680px) {
        nav { padding: 0 1rem; }
        .brand-name { display: none; }
        .container { padding: 1rem; }
        .stats-row { grid-template-columns: repeat(3, 1fr); gap: .5rem; }
        .stat-num { font-size: 1.5rem; }
        .tag-name { max-width: 160px; }
    }
    @media (max-width: 420px) {
        .stats-row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
"""
    + _NAV_HTML
    + """
<div class="container">
"""
    + _FLASH_HTML
    + """
  <div class="page-header">
    <div class="page-title-group">
      <div class="page-title">Tags</div>
      <div class="page-sub">All tags used and their frequency</div>
    </div>
  </div>

  <div class="stats-row">
    <div class="stat-card">
      <div class="stat-num">{{ total_tags }}</div>
      <div class="stat-label">Various Tags</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">{{ total_usages }}</div>
      <div class="stat-label">Usages</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">{{ "%.1f"|format(total_usages / total_tags if total_tags > 0 else 0) }}</div>
      <div class="stat-label">Ø per Tag</div>
    </div>
  </div>

  <div class="tag-toolbar">
    <div class="tag-search-wrap">
      <span class="s-icon">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8">
          <circle cx="6.5" cy="6.5" r="4.5"/><path d="M10.5 10.5l3 3"/>
        </svg>
      </span>
      <input type="text" id="tagSearch" placeholder="Filter tags…" oninput="filterTags()">
    </div>
    <span id="tagCount" class="tag-count-display">{{ total_tags }} Tags</span>
  </div>

  {% if tag_stats %}
    <div class="tag-list" id="tagsContainer">
      {% set max_count = tag_stats[0][1] if tag_stats else 1 %}
      {% for tag, count in tag_stats %}
        {%- set dot_cls = 'is-user' if tag.startswith('user:') else ('is-type' if tag in ['image','gif','video'] else 'is-other') -%}
        <div class="tag-item" data-tag="{{ tag.lower() }}">
          <span class="tag-dot {{ dot_cls }}"></span>
          <span class="tag-name {% if tag.startswith('user:') %}is-user{% elif tag in ['image','gif','video'] %}is-type{% endif %}">{{ tag }}</span>
          <div class="tag-bar-track">
            <div class="tag-bar-fill" style="width:{{ (count / max_count * 100)|round(1) }}%"></div>
          </div>
          <span class="tag-count">{{ count }}</span>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <div class="no-tags-msg">
      <div class="empty-icon">&#127991;</div>
      <p>No tags yet</p>
      <p>Tags are assigned during upload or can be added later.</p>
    </div>
  {% endif %}
</div>

<script>
  let visibleCount = {{ total_tags }};
  const totalCount = {{ total_tags }};

  function filterTags() {
      const q = document.getElementById('tagSearch').value.toLowerCase();
      let count = 0;
      document.querySelectorAll('.tag-item').forEach(el => {
          const show = el.dataset.tag.includes(q);
          el.style.display = show ? '' : 'none';
          if (show) count++;
      });
      const countEl = document.getElementById('tagCount');
      if (countEl) countEl.textContent = count + (q ? ' von ' + totalCount : '') + ' Tags';
  }

  document.querySelectorAll('.tag-item').forEach(el => {
      el.addEventListener('click', function () {
          const tag = this.querySelector('.tag-name').textContent.trim();
          window.location.href = '{{ url_for("index") }}?search=' + encodeURIComponent(tag);
      });
  });
</script>
</body>
</html>"""
)

# ---------------------------------------------------------------------------
#  Feed (TikTok-style endless shuffle)
# ---------------------------------------------------------------------------
TEMPLATE_FEED = (
    """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>MediaIndex — Feed</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="csrf-token" content="{{ csrf_token() }}"/>
  <style>"""
    + _COMMON_CSS
    + """
    html, body { height: 100%; overflow: hidden; }
    body { background: #000; }

    /* Make the global gradient absent on feed */
    body { background-image: none; }

    .feed-container {
        height: calc(100vh - 58px);
        height: calc(100dvh - 58px);
        overflow-y: scroll;
        scroll-snap-type: y mandatory;
        scroll-behavior: smooth;
        scrollbar-width: none;
        -ms-overflow-style: none;
        background: #000;
    }
    .feed-container::-webkit-scrollbar { display: none; }

    .feed-slide {
        height: calc(100vh - 58px);
        height: calc(100dvh - 58px);
        width: 100%;
        scroll-snap-align: start;
        scroll-snap-stop: always;
        position: relative;
        background: #000;
        overflow: hidden;
    }

    .feed-media,
    video.feed-media,
    img.feed-media {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100% !important;
        height: 100% !important;
        max-width: 100% !important;
        max-height: 100% !important;
        object-fit: contain !important;
        object-position: center center !important;
        display: block !important;
        margin: 0 !important;
    }

    /* Soft gradient backdrop so portrait media doesn't look bare */
    .feed-slide::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at center, rgba(124,106,255,.06), transparent 60%);
        pointer-events: none;
    }

    /* Bottom info overlay */
    .feed-overlay {
        position: absolute;
        left: 0; right: 0; bottom: 0;
        padding: 1.25rem 1.5rem 1.5rem;
        background: linear-gradient(to top, rgba(0,0,0,.85) 0%, rgba(0,0,0,.5) 60%, transparent 100%);
        z-index: 3;
        pointer-events: none;
    }
    .feed-uploader {
        font-size: .82rem;
        color: var(--text2);
        margin-bottom: .55rem;
        display: flex;
        align-items: center;
        gap: .5rem;
        letter-spacing: -.01em;
    }
    .feed-uploader .user-avatar {
        width: 24px; height: 24px;
        font-size: .7rem;
    }
    .feed-tags {
        display: flex;
        flex-wrap: wrap;
        gap: .3rem;
        max-width: calc(100% - 80px);
        pointer-events: auto;
    }

    /* Right-side action rail */
    .feed-actions {
        position: absolute;
        right: 1rem;
        bottom: 5rem;
        display: flex;
        flex-direction: column;
        gap: .65rem;
        z-index: 4;
    }
    .feed-btn {
        width: 46px; height: 46px;
        border-radius: 50%;
        background: rgba(20,22,30,.6);
        border: 1px solid rgba(255,255,255,.12);
        color: var(--text);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.05rem;
        cursor: pointer;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: background .15s, border-color .15s, transform .15s;
        text-decoration: none;
    }
    .feed-btn:hover {
        background: rgba(124,106,255,.25);
        border-color: var(--border-hi);
        transform: scale(1.05);
    }
    .feed-btn.is-danger:hover {
        background: rgba(248,81,73,.25);
        border-color: rgba(248,81,73,.5);
        color: var(--danger);
    }
    .feed-btn.is-active {
        background: rgba(124,106,255,.3);
        border-color: var(--border-hi);
        color: #fff;
    }

    /* Type badge top-left */
    .feed-type {
        position: absolute;
        top: 1rem; left: 1rem;
        padding: .25em .65em;
        border-radius: 5px;
        font-size: .7rem;
        font-weight: 700;
        letter-spacing: .04em;
        text-transform: uppercase;
        backdrop-filter: blur(8px);
        z-index: 3;
    }
    .feed-type.video { background: rgba(92,124,255,.55); color: #c0cfff; border: 1px solid rgba(92,124,255,.3); }
    .feed-type.gif   { background: rgba(168,85,247,.55); color: #e8c5ff; border: 1px solid rgba(168,85,247,.3); }
    .feed-type.image { background: rgba(20,160,120,.55); color: #a0f0d8; border: 1px solid rgba(20,160,120,.3); }

    /* Mute indicator */
    .mute-hint {
        position: absolute;
        top: 1rem; right: 1rem;
        padding: .35rem .7rem;
        border-radius: 99px;
        font-size: .72rem;
        background: rgba(20,22,30,.65);
        border: 1px solid rgba(255,255,255,.12);
        color: var(--text2);
        backdrop-filter: blur(10px);
        z-index: 3;
        opacity: 0;
        transition: opacity .25s;
        pointer-events: none;
    }
    .feed-slide.has-video .mute-hint { opacity: 1; }

    /* Loading sentinel slide */
    .feed-loader-slide {
        height: calc(100vh - 58px);
        height: calc(100dvh - 58px);
        scroll-snap-align: start;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: .75rem;
        color: var(--muted);
        font-size: .85rem;
    }
    .feed-loader {
        width: 28px; height: 28px;
        border: 2.5px solid var(--border2);
        border-top-color: var(--accent);
        border-radius: 50%;
        animation: spin .7s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* Empty state */
    .feed-empty {
        height: calc(100vh - 58px);
        height: calc(100dvh - 58px);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: .5rem;
        color: var(--muted);
        text-align: center;
        padding: 2rem;
    }
    .feed-empty .empty-icon { font-size: 3rem; opacity: .25; }

    /* Tag pill (override common, ensure visibility on dark bg) */
    .feed-tags .tag-pill {
        background: rgba(124,106,255,.18);
        color: #d8d0ff;
        border: 1px solid rgba(124,106,255,.32);
        font-size: .72rem;
        padding: .15em .55em;
    }
    .feed-tags .tag-pill.user-tag {
        background: rgba(210,153,34,.18);
        color: #f5d27a;
        border-color: rgba(210,153,34,.35);
    }
    .feed-tags .tag-pill.type-tag {
        background: rgba(63,185,80,.18);
        color: #8be098;
        border-color: rgba(63,185,80,.35);
    }

    /* Scroll hint on first slide */
    .scroll-hint {
        position: absolute;
        bottom: 1.25rem;
        left: 50%;
        transform: translateX(-50%);
        font-size: .72rem;
        color: var(--muted);
        letter-spacing: .08em;
        text-transform: uppercase;
        opacity: .7;
        animation: bounce 1.6s ease-in-out infinite;
        z-index: 3;
        pointer-events: none;
    }
    @keyframes bounce {
        0%,100% { transform: translate(-50%, 0); }
        50%     { transform: translate(-50%, -6px); }
    }

    @media (max-width: 680px) {
        .feed-overlay { padding: 1rem 1rem 1.25rem; }
        .feed-actions { right: .65rem; bottom: 4.5rem; gap: .5rem; }
        .feed-btn { width: 42px; height: 42px; font-size: 1rem; }
        .feed-tags { max-width: calc(100% - 60px); }
    }
  </style>
</head>
<body>
"""
    + _NAV_HTML
    + """
<div class="feed-container" id="feedContainer">
  <div class="feed-loader-slide" id="initialLoader">
    <div class="feed-loader"></div>
    <div>Loading feed…</div>
  </div>
</div>

<script>
  const csrfToken = () => document.querySelector('meta[name="csrf-token"]').content;

  const container = document.getElementById('feedContainer');
  const initialLoader = document.getElementById('initialLoader');

  // Random seed per visit so the order changes each time the page is opened.
  let seed = Math.floor(Math.random() * 2147483647);
  let page = 0;
  let loading = false;
  let exhausted = false;
  let muted = true;
  let firstLoad = true;

  function esc(s) {
      return (s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;')
                     .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function makeTagPills(tagsStr) {
      if (!tagsStr) return '';
      return tagsStr.split(',').filter(t => t.trim()).map(t => {
          const tag = t.trim();
          let cls = 'tag-pill';
          if (tag.startsWith('user:')) cls += ' user-tag';
          else if (['image','gif','video'].includes(tag)) cls += ' type-tag';
          return `<span class="${cls}">${esc(tag)}</span>`;
      }).join('');
  }

  function buildSlide(m) {
      const slide = document.createElement('div');
      slide.className = 'feed-slide';
      slide.dataset.id = m.id;
      slide.dataset.type = m.type;
      slide.dataset.filepath = m.filepath;
      // Bulletproof inline styles for the slide too.
      const slideH = (window.innerHeight - 58) + 'px';
      Object.assign(slide.style, {
          position: 'relative',
          width: '100%',
          height: slideH,
          minHeight: slideH,
          background: '#000',
          overflow: 'hidden',
          scrollSnapAlign: 'start',
          scrollSnapStop: 'always',
      });

      const isVideo = m.type === 'video';
      if (isVideo) slide.classList.add('has-video');

      const initial = (m.uploaded_by || '?')[0].toUpperCase();

      slide.innerHTML = `
        <span class="feed-type ${esc(m.type)}">${esc(m.type)}</span>
        ${isVideo ? '<div class="mute-hint" data-mute-hint>🔇 Tap to unmute</div>' : ''}
        <div class="feed-actions">
          <a class="feed-btn" href="/media/${esc(m.filepath)}" download="${esc(m.filepath)}" title="Download">↓</a>
          <button class="feed-btn is-danger" onclick="deleteSlide(${m.id})" title="Delete">×</button>
        </div>
        <div class="feed-overlay">
          <div class="feed-uploader">
            <div class="user-avatar">${esc(initial)}</div>
            <span>${esc(m.uploaded_by || 'Unknown')}</span>
          </div>
          <div class="feed-tags">${makeTagPills(m.tags)}</div>
        </div>
      `;

      const mediaEl = document.createElement(isVideo ? 'video' : 'img');
      mediaEl.className = 'feed-media';
      mediaEl.dataset.src = '/media/' + m.filepath;
      // Bulletproof inline styles — beat any cached/conflicting CSS.
      Object.assign(mediaEl.style, {
          position: 'absolute',
          top: '0',
          left: '0',
          right: '0',
          bottom: '0',
          width: '100%',
          height: '100%',
          maxWidth: '100%',
          maxHeight: '100%',
          objectFit: 'contain',
          objectPosition: 'center center',
          display: 'block',
          margin: '0',
      });
      if (isVideo) {
          mediaEl.muted = muted;
          mediaEl.loop = true;
          mediaEl.playsInline = true;
          mediaEl.preload = 'metadata';
          mediaEl.addEventListener('click', () => toggleMute(slide));
      } else {
          mediaEl.alt = '';
      }
      slide.insertBefore(mediaEl, slide.firstChild);

      return slide;
  }

  function toggleMute(slide) {
      muted = !muted;
      document.querySelectorAll('.feed-slide video').forEach(v => v.muted = muted);
      const hint = slide.querySelector('[data-mute-hint]');
      if (hint) {
          hint.textContent = muted ? '🔇 Tap to unmute' : '🔊 Sound on';
          hint.style.opacity = '1';
          clearTimeout(hint._t);
          hint._t = setTimeout(() => { hint.style.opacity = ''; }, 1500);
      }
  }

  function deleteSlide(id) {
      if (!confirm('Are you sure you want to delete this file?')) return;
      const fd = new FormData();
      fetch(`/delete/${id}`, { method: 'POST', headers: {'X-CSRFToken': csrfToken()} })
          .then(r => {
              if (!r.ok) throw new Error('fail');
              const slide = container.querySelector(`.feed-slide[data-id="${id}"]`);
              if (slide) slide.remove();
          })
          .catch(() => alert('Error deleting file.'));
  }

  // Lazy-load real src once a slide is near
  const lazyMediaObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
          if (!e.isIntersecting) return;
          const el = e.target.querySelector('.feed-media');
          if (el && el.dataset.src && !el.src) el.src = el.dataset.src;
          lazyMediaObs.unobserve(e.target);
      });
  }, { root: container, rootMargin: '300px 0px', threshold: 0.01 });

  // Play/pause videos as they enter/leave the viewport
  const playObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
          const v = e.target.querySelector('video');
          if (!v) return;
          if (e.isIntersecting && e.intersectionRatio > 0.6) {
              v.muted = muted;
              const p = v.play();
              if (p && p.catch) p.catch(() => {});
          } else {
              v.pause();
          }
      });
  }, { root: container, threshold: [0, 0.6, 1] });

  // Trigger more loads when sentinel appears
  const sentinelObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
          if (e.isIntersecting) loadMore();
      });
  }, { root: container, rootMargin: '600px 0px' });

  function loadMore() {
      if (loading || exhausted) return;
      loading = true;
      page++;
      const url = new URL('/api/feed', location.origin);
      url.searchParams.set('seed', seed);
      url.searchParams.set('page', page);
      fetch(url).then(r => r.json()).then(data => {
          if (firstLoad) {
              firstLoad = false;
              if (initialLoader) initialLoader.remove();
              if (!data.media || data.media.length === 0) {
                  const empty = document.createElement('div');
                  empty.className = 'feed-empty';
                  empty.innerHTML = `
                    <div class="empty-icon">&#128247;</div>
                    <div>No media yet</div>
                    <div style="font-size:.78rem;">Upload something to start the feed.</div>
                  `;
                  container.appendChild(empty);
                  exhausted = true;
                  loading = false;
                  return;
              }
          }
          // remove any existing trailing sentinel
          const oldSentinel = document.getElementById('feedSentinel');
          if (oldSentinel) oldSentinel.remove();

          (data.media || []).forEach((m, idx) => {
              const slide = buildSlide(m);
              container.appendChild(slide);
              lazyMediaObs.observe(slide);
              playObs.observe(slide);
              if (firstLoad === false && page === 1 && idx === 0) {
                  const hint = document.createElement('div');
                  hint.className = 'scroll-hint';
                  hint.textContent = 'Scroll ↓';
                  slide.appendChild(hint);
                  setTimeout(() => hint.remove(), 4000);
              }
          });

          if (data.has_more) {
              const sentinel = document.createElement('div');
              sentinel.id = 'feedSentinel';
              sentinel.className = 'feed-loader-slide';
              sentinel.innerHTML = '<div class="feed-loader"></div><div>Loading more…</div>';
              container.appendChild(sentinel);
              sentinelObs.observe(sentinel);
          } else {
              // Re-shuffle for true endlessness: reset with a fresh seed
              seed = Math.floor(Math.random() * 2147483647);
              page = 0;
              const sentinel = document.createElement('div');
              sentinel.id = 'feedSentinel';
              sentinel.className = 'feed-loader-slide';
              sentinel.innerHTML = '<div class="feed-loader"></div><div>Reshuffling…</div>';
              container.appendChild(sentinel);
              sentinelObs.observe(sentinel);
          }
          loading = false;
      }).catch((err) => {
          console.error('feed load failed', err);
          loading = false;
      });
  }

  // Resize handler — keep all slides matched to the current viewport.
  window.addEventListener('resize', () => {
      const h = (window.innerHeight - 58) + 'px';
      container.style.height = h;
      document.querySelectorAll('.feed-slide').forEach(s => {
          s.style.height = h;
          s.style.minHeight = h;
      });
  });
  // Lock the container height too.
  container.style.height = (window.innerHeight - 58) + 'px';

  // Kick off
  loadMore();

  // Keyboard nav (j/k or arrow keys)
  document.addEventListener('keydown', e => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
      const slides = [...container.querySelectorAll('.feed-slide')];
      if (!slides.length) return;
      const top = container.scrollTop;
      const slideH = slides[0].clientHeight || 1;
      const idx = Math.round(top / slideH);
      let target = idx;
      if (e.key === 'ArrowDown' || e.key === 'j') target = Math.min(idx + 1, slides.length - 1);
      else if (e.key === 'ArrowUp' || e.key === 'k') target = Math.max(idx - 1, 0);
      else if (e.key === 'm') {
          muted = !muted;
          document.querySelectorAll('.feed-slide video').forEach(v => v.muted = muted);
          return;
      } else return;
      e.preventDefault();
      slides[target].scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
</script>
</body>
</html>"""
)
