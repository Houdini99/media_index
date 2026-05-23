"""All raw SQL for the media domain.

Routes never embed SQL — they call the functions in this module. The schema,
ALTER-TABLE migrations, and WHERE-clause builder are preserved exactly as in
the original main.py.
"""
import logging
import os
import sqlite3
from datetime import datetime

from ..config import Config


def _conn():
    return sqlite3.connect(Config.DB_FILE)


def _auth_conn():
    return sqlite3.connect(Config.AUTH_DB)


# ── Schema / migrations ────────────────────────────────────────────────────
def init_media_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filepath TEXT NOT NULL,
        thumb TEXT,
        tags TEXT,
        filehash TEXT UNIQUE,
        uploaded_by INTEGER,
        upload_date TEXT,
        is_private INTEGER NOT NULL DEFAULT 0
    );
    """)
    cur.execute("PRAGMA table_info(media)")
    cols = [c[1] for c in cur.fetchall()]
    if 'uploaded_by' not in cols:
        cur.execute("ALTER TABLE media ADD COLUMN uploaded_by INTEGER")
    if 'upload_date' not in cols:
        cur.execute("ALTER TABLE media ADD COLUMN upload_date TEXT")
    if 'is_private' not in cols:
        cur.execute("ALTER TABLE media ADD COLUMN is_private INTEGER NOT NULL DEFAULT 0")
    conn.commit()
    conn.close()


# ── Username helpers (cross-DB read against AUTH_DB) ───────────────────────
def get_username_by_id(uid):
    if not uid:
        return None
    try:
        conn = _auth_conn()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE id=?", (uid,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None
    except Exception as e:
        logging.warning("get_username_by_id failed for uid=%s: %s", uid, e)
        return None


def get_usernames_for_media(data):
    ids = {m[5] for m in data if len(m) > 5 and m[5]}
    if not ids:
        return {}
    try:
        conn = _auth_conn()
        cur = conn.cursor()
        ph = ','.join('?' * len(ids))
        cur.execute(f"SELECT id,username FROM users WHERE id IN ({ph})", list(ids))
        um = {uid: name for uid, name in cur.fetchall()}
        conn.close()
        return um
    except Exception as e:
        logging.warning("get_usernames_for_media failed: %s", e)
        return {}


# ── Shared WHERE-clause builder ────────────────────────────────────────────
def _build_where(ft, search, exclude_tags, include_tags=None, viewer_id=None, private_only=False):
    """Build shared WHERE clause components for media queries.

    `ft` may be a single value ('all'|'image'|'gif'|'video') or a comma-
    separated list of types, in which case the matching extensions are OR-ed.

    `viewer_id`, when set, hides rows marked is_private=1 unless they were
    uploaded by the viewer themselves.

    `private_only`, when truthy together with `viewer_id`, restricts the
    result to the viewer's *own* private uploads only.
    """
    conds, params = [], []
    if private_only and viewer_id is not None:
        conds.append("(is_private = 1 AND uploaded_by = ?)")
        params.append(viewer_id)
    elif viewer_id is not None:
        conds.append("(is_private = 0 OR uploaded_by = ?)")
        params.append(viewer_id)
    types = []
    if ft and ft != 'all':
        types = [t.strip() for t in str(ft).split(',') if t.strip() and t.strip() != 'all']
    if types:
        type_clauses = []
        for t in types:
            if t == 'image':
                type_clauses.append("(" + " OR ".join(f"filepath LIKE '%.{e}'" for e in Config.ALLOWED_IMAGE_EXT) + ")")
            elif t == 'video':
                type_clauses.append("(" + " OR ".join(f"filepath LIKE '%.{e}'" for e in Config.ALLOWED_VIDEO_EXT) + ")")
            elif t == 'gif':
                type_clauses.append("filepath LIKE '%.gif'")
        if type_clauses:
            conds.append("(" + " OR ".join(type_clauses) + ")")
    if search:
        conds.append("tags LIKE ?")
        params.append(f"%{search}%")
    if include_tags:
        for tag in [t.strip() for t in include_tags.split(',') if t.strip()]:
            # Whole-tag match using comma-padded haystack (same trick as exclude).
            conds.append("(tags IS NOT NULL AND (',' || tags || ',') LIKE ?)")
            params.append(f"%,{tag},%")
    if exclude_tags:
        for tag in [t.strip() for t in exclude_tags.split(',') if t.strip()]:
            # Match whole tag only by padding the stored tags with commas on both sides,
            # so "ai" won't match "portainer" or any other tag that merely contains the word.
            conds.append("(tags IS NULL OR (',' || tags || ',') NOT LIKE ?)")
            params.append(f"%,{tag},%")
    return conds, params


# ── Read queries ───────────────────────────────────────────────────────────
def get_media_count(ft=None, search=None, exclude_tags=None, include_tags=None, viewer_id=None, private_only=False):
    conds, params = _build_where(ft, search, exclude_tags, include_tags, viewer_id, private_only)
    conn = _conn()
    cur = conn.cursor()
    q = "SELECT COUNT(*) FROM media"
    if conds:
        q += " WHERE " + " AND ".join(conds)
    cur.execute(q, params)
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_media(ft=None, search=None, exclude_tags=None, page=1, include_tags=None, viewer_id=None, private_only=False):
    conds, params = _build_where(ft, search, exclude_tags, include_tags, viewer_id, private_only)
    conn = _conn()
    cur = conn.cursor()
    q = "SELECT * FROM media"
    if conds:
        q += " WHERE " + " AND ".join(conds)
    q += " ORDER BY id DESC"
    q += f" LIMIT {Config.PAGE_SIZE} OFFSET {(page - 1) * Config.PAGE_SIZE}"
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


def get_media_ids(ft=None, search=None, exclude_tags=None, include_tags=None, viewer_id=None):
    conds, params = _build_where(ft, search, exclude_tags, include_tags, viewer_id)
    conn = _conn()
    cur = conn.cursor()
    q = "SELECT id FROM media"
    if conds:
        q += " WHERE " + " AND ".join(conds)
    cur.execute(q, params)
    ids = [r[0] for r in cur.fetchall()]
    conn.close()
    return ids


def get_media_by_ids(ids, viewer_id=None):
    if not ids:
        return []
    conn = _conn()
    cur = conn.cursor()
    ph = ','.join('?' * len(ids))
    q = f"SELECT * FROM media WHERE id IN ({ph})"
    params = list(ids)
    if viewer_id is not None:
        q += " AND (is_private = 0 OR uploaded_by = ?)"
        params.append(viewer_id)
    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    by_id = {r[0]: r for r in rows}
    return [by_id[i] for i in ids if i in by_id]


def get_media_by_id(mid, viewer_id=None):
    conn = _conn()
    cur = conn.cursor()
    if viewer_id is not None:
        cur.execute(
            "SELECT * FROM media WHERE id=? AND (is_private = 0 OR uploaded_by = ?)",
            (mid, viewer_id),
        )
    else:
        cur.execute("SELECT * FROM media WHERE id=?", (mid,))
    m = cur.fetchone()
    conn.close()
    return m


def get_privacy_for_file(fname):
    """Return (uploaded_by, is_private) for the media row whose stored
    filepath or thumb ends with `fname`, or None if no such row exists.
    Used by the file-serving routes to block direct access to private media.
    """
    if not fname:
        return None
    needle = f"%/{fname}"
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT uploaded_by, COALESCE(is_private, 0) FROM media "
        "WHERE filepath LIKE ? OR thumb LIKE ? OR filepath = ? OR thumb = ? "
        "LIMIT 1",
        (needle, needle, fname, fname),
    )
    row = cur.fetchone()
    conn.close()
    return row


def hash_exists(fh):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM media WHERE filehash=?", (fh,))
    row = cur.fetchone()
    conn.close()
    return row is not None


def get_tag_statistics(viewer_id=None):
    """Get all tags and their counts from the database.

    When `viewer_id` is set, tags on private media uploaded by other users
    are excluded so the tag cloud can't leak private content.
    """
    conn = _conn()
    cur = conn.cursor()
    if viewer_id is not None:
        cur.execute(
            "SELECT tags FROM media WHERE tags IS NOT NULL AND tags != '' "
            "AND (is_private = 0 OR uploaded_by = ?)",
            (viewer_id,),
        )
    else:
        cur.execute("SELECT tags FROM media WHERE tags IS NOT NULL AND tags != ''")
    rows = cur.fetchall()
    conn.close()

    tag_counts = {}
    for (tags_str,) in rows:
        if tags_str:
            tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    sorted_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0].lower()))
    return sorted_tags


# ── Write queries ──────────────────────────────────────────────────────────
def insert_media(fp, th, tags, fh, uid, is_private=False):
    conn = _conn()
    cur = conn.cursor()
    try:
        udate = datetime.now().isoformat()
        uname = get_username_by_id(uid)
        if uname and f"user:{uname}" not in (tags or ""):
            tags = f"{tags},user:{uname}" if tags else f"user:{uname}"
        cur.execute(
            "INSERT INTO media (filepath,thumb,tags,filehash,uploaded_by,upload_date,is_private) "
            "VALUES (?,?,?,?,?,?,?)",
            (fp, th, tags, fh, uid, udate, 1 if is_private else 0)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def delete_media(mid, user_id):
    conn = _conn()
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


def update_media_tags(mid, new_tags, user_id):
    conn = _conn()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE media SET tags=? WHERE id=? AND uploaded_by=?", (new_tags, mid, user_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()
