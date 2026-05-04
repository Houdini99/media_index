"""Media routes — gallery, upload, feed, tags, and JSON APIs.

All persistence calls go through app.media.db; image/video processing
calls go through app.media.processing.
"""
import os
import random
import tempfile
from flask import (
    render_template, request, redirect, url_for, flash,
    send_from_directory, jsonify, g
)
from werkzeug.utils import secure_filename

from . import media_bp
from .db import (
    get_media,
    get_media_count,
    get_media_ids,
    get_media_by_ids,
    get_media_by_id,
    get_usernames_for_media,
    get_username_by_id,
    get_tag_statistics,
    hash_exists,
    insert_media,
    delete_media,
    update_media_tags,
)
from .processing import (
    allowed_file,
    file_type,
    sha256_file,
    gen_image_thumb,
    gen_video_thumb,
    gen_placeholder_thumb,
)
from ..auth.routes import login_required
from ..config import Config


# ── Pages ─────────────────────────────────────────────────────────────────
@media_bp.route('/')
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
    return render_template(
        'index.html',
        media=media,
        search=request.args.get('search', ''),
        exclude_tags=request.args.get('exclude_tags', ''),
        filter_type=request.args.get('type', 'all'),
        hide_ai=hide_ai
    )


@media_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        results = {'uploaded': [], 'duplicates': [], 'errors': []}
        uid = g.user['id'] if g.user else None
        if not uid:
            flash("❌ Fehler: Nicht eingeloggt.", "danger")
            return redirect(url_for('media.upload'))
        for i, f in enumerate(files):
            fn = secure_filename(f.filename)
            if not fn or not allowed_file(fn):
                results['errors'].append(fn); continue
            tags = request.form.get(f'tags_{i}', '')
            ext = fn.rsplit('.', 1)[-1].lower()
            with tempfile.NamedTemporaryFile(dir=Config.UPLOAD_FOLDER, delete=False, suffix=f'.{ext}') as tf:
                tmp = tf.name
            f.save(tmp)
            fh = sha256_file(tmp)
            if hash_exists(fh):
                os.remove(tmp)
                results['duplicates'].append(fn); continue
            final = os.path.join(Config.UPLOAD_FOLDER, f"{fh}.{ext}")
            os.rename(tmp, final)
            tname = f"{fh}.png"
            tpath = os.path.join(Config.THUMB_FOLDER, tname)
            if ext in Config.ALLOWED_IMAGE_EXT | Config.ALLOWED_GIF_EXT:
                gen_image_thumb(final, tpath)
            elif ext in Config.ALLOWED_VIDEO_EXT:
                gen_video_thumb(final, tpath)
            else:
                gen_placeholder_thumb(tpath)
            if insert_media(final, tpath, ','.join(filter(None, [tags, file_type(fn)])), fh, uid):
                results['uploaded'].append(fn)
            else:
                results['errors'].append(fn)
        for k, v in results.items():
            if v:
                if k == 'uploaded':
                    flash(f"✅Successful: {', '.join(v)}", "success")
                elif k == 'duplicates':
                    flash(f"⚠️ Duplicates: {', '.join(v)}", "warning")
                else:
                    flash(f"❌ Error: {', '.join(v)}", "danger")
        return redirect(url_for('media.upload'))
    return render_template('upload.html')


@media_bp.route('/feed')
@login_required
def feed():
    return render_template('feed.html')


@media_bp.route('/tags')
@login_required
def tags():
    """Show tag statistics page"""
    tag_stats = get_tag_statistics()
    total_tags = len(tag_stats)
    total_usages = sum(count for _, count in tag_stats)
    return render_template(
        'tags.html',
        tag_stats=tag_stats,
        total_tags=total_tags,
        total_usages=total_usages
    )


# ── File serving ──────────────────────────────────────────────────────────
@media_bp.route('/thumbs/<fname>')
@login_required
def serve_thumb(fname):
    return send_from_directory(Config.THUMB_FOLDER, fname)


@media_bp.route('/media/<fname>')
@login_required
def serve_media(fname):
    return send_from_directory(Config.UPLOAD_FOLDER, fname)


# ── Mutations ─────────────────────────────────────────────────────────────
@media_bp.route('/delete/<int:media_id>', methods=['POST'])
@login_required
def delete(media_id):
    if delete_media(media_id, g.user['id']):
        flash("✅ File deleted.", "success")
    else:
        flash("❌ Error deleting file.", "danger")
    return redirect(url_for('media.index'))


@media_bp.route('/edit/<int:media_id>', methods=['POST'])
@login_required
def edit_tags(media_id):
    new_tags = request.form.get('tags', '').strip()
    if update_media_tags(media_id, new_tags, g.user['id']):
        flash("✅ Tags successfully updated.", "success")
    else:
        flash("❌ Error updating tags.", "danger")
    return redirect(url_for('media.index'))


# ── JSON APIs ─────────────────────────────────────────────────────────────
@media_bp.route('/mediadata/<int:media_id>')
@login_required
def media_meta(media_id):
    m = get_media_by_id(media_id)
    if m:
        uid = m[5]
        return jsonify({
            'id': m[0],
            'filepath': url_for('media.serve_media', fname=os.path.basename(m[1])),
            'thumb': url_for('media.serve_thumb', fname=os.path.basename(m[2])),
            'tags': m[3],
            'type': file_type(m[1]),
            'uploaded_by': get_username_by_id(uid) or 'Unknown',
            'upload_date': m[6]
        })
    return jsonify({'error': 'Not found'}), 404


@media_bp.route('/api/media')
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
    has_more = (page * Config.PAGE_SIZE) < total
    result = [
        {'id': m[0], 'thumb': os.path.basename(m[2]), 'tags': m[3] or '', 'type': file_type(m[1])}
        for m in media
    ]
    return jsonify({'media': result, 'has_more': has_more})


@media_bp.route('/api/feed')
@login_required
def api_feed():
    # `types` (comma-separated) takes precedence over the legacy single `type`.
    ft = request.args.get('types') or request.args.get('type', 'all')
    search = request.args.get('search', '')
    include_tags = request.args.get('include_tags', '')
    hide_ai = request.args.get('hide_ai', '')
    exclude_tags = request.args.get('exclude_tags', '')
    if hide_ai == '1':
        ai_tags = 'fake,ai,grok,deepfake,gemini,chatgpt'
        exclude_tags = (exclude_tags + ',' + ai_tags).strip(',') if exclude_tags else ai_tags
    try:
        seed = int(request.args.get('seed', '0'))
    except (ValueError, TypeError):
        seed = 0
    try:
        page = max(1, min(int(request.args.get('page', 1)), 99999))
    except (ValueError, TypeError):
        page = 1

    ids = get_media_ids(ft, search, exclude_tags, include_tags=include_tags)
    rng = random.Random(seed)
    rng.shuffle(ids)

    start = (page - 1) * Config.PAGE_SIZE
    end = start + Config.PAGE_SIZE
    page_ids = ids[start:end]
    has_more = end < len(ids)

    rows = get_media_by_ids(page_ids)
    umap = get_usernames_for_media(rows)
    result = [
        {
            'id': m[0],
            'filepath': os.path.basename(m[1]),
            'thumb': os.path.basename(m[2]),
            'tags': m[3] or '',
            'type': file_type(m[1]),
            'uploaded_by': umap.get(m[5], 'Unknown'),
        }
        for m in rows
    ]
    return jsonify({'media': result, 'has_more': has_more, 'total': len(ids)})


@media_bp.route('/api/tags')
@login_required
def api_tags():
    tag_stats = get_tag_statistics()
    return jsonify(sorted(tag for tag, _ in tag_stats))
