const csrfToken = () => document.querySelector('meta[name="csrf-token"]').content;

const container = document.getElementById('feedContainer');
const initialLoader = document.getElementById('initialLoader');

const STORAGE_KEY = 'mediaindex.feedSettings';
const DEFAULT_SETTINGS = {
    types: ['image', 'gif', 'video'],
    includeTags: '',
    excludeTags: '',
    volume: 1.0,
    muted: true,
};

function loadSettings() {
    try {
        const raw = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
        const merged = { ...DEFAULT_SETTINGS, ...raw };
        if (!Array.isArray(merged.types) || !merged.types.length) merged.types = [...DEFAULT_SETTINGS.types];
        merged.volume = Math.max(0, Math.min(1, Number(merged.volume) || 0));
        merged.muted = !!merged.muted;
        return merged;
    } catch (_) {
        return { ...DEFAULT_SETTINGS };
    }
}
function saveSettings() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(settings)); } catch (_) {}
}

const settings = loadSettings();

let seed = Math.floor(Math.random() * 2147483647);
let page = 0;
let loading = false;
let exhausted = false;
let firstLoad = true;

function esc(s) {
    return (s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;')
                   .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function fmtTime(t) {
    if (!isFinite(t) || isNaN(t) || t < 0) return '0:00';
    const m = Math.floor(t / 60);
    const s = Math.floor(t % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
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

    const privateBadge = m.is_private
        ? `<span class="feed-type private" title="Only visible to you">private</span>`
        : '';
    const dlName = m.download_name || m.filepath;
    slide.innerHTML = `
      <span class="feed-type ${esc(m.type)}">${esc(m.type)}</span>
      ${privateBadge}
      <div class="feed-actions">
        <a class="feed-btn" href="/media/${esc(m.filepath)}" download="${esc(dlName)}" title="Download">↓</a>
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
    Object.assign(mediaEl.style, {
        position: 'absolute',
        top: '0', left: '0', right: '0', bottom: '0',
        width: '100%', height: '100%',
        maxWidth: '100%', maxHeight: '100%',
        objectFit: 'contain',
        objectPosition: 'center center',
        display: 'block',
        margin: '0',
    });
    if (isVideo) {
        mediaEl.muted = settings.muted;
        mediaEl.volume = settings.volume;
        mediaEl.loop = true;
        mediaEl.playsInline = true;
        mediaEl.preload = 'metadata';
        mediaEl.addEventListener('click', () => toggleMute());
    } else {
        mediaEl.alt = '';
    }
    slide.insertBefore(mediaEl, slide.firstChild);

    if (isVideo) attachVideoProgress(slide, mediaEl);

    return slide;
}

// ── Video progress bar (per-slide) ────────────────────────────────────────
// One shared drag state + a single pair of document listeners. The old code
// attached mousemove/mouseup to `document` *per slide*, leaking one handler for
// every video ever built — so a long feed ran hundreds of them on each move.
let activeProgressDrag = null;

function progressSeek(drag, e) {
    const rect = drag.track.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const pct = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
    if (drag.video.duration) drag.video.currentTime = pct * drag.video.duration;
}
function endProgressDrag() {
    if (!activeProgressDrag) return;
    activeProgressDrag.bar.classList.remove('is-dragging');
    activeProgressDrag = null;
}
document.addEventListener('mousemove', (e) => { if (activeProgressDrag) progressSeek(activeProgressDrag, e); });
document.addEventListener('mouseup', endProgressDrag);

function attachVideoProgress(slide, video) {
    const bar = document.createElement('div');
    bar.className = 'feed-progress';
    bar.innerHTML = `
      <div class="feed-progress-time">
        <span data-progress-current>0:00</span>
        <span data-progress-total>0:00</span>
      </div>
      <div class="feed-progress-track" data-progress-track>
        <div class="feed-progress-fill" data-progress-fill></div>
        <div class="feed-progress-handle" data-progress-handle></div>
      </div>
    `;
    slide.appendChild(bar);

    const track = bar.querySelector('[data-progress-track]');
    const fill = bar.querySelector('[data-progress-fill]');
    const handle = bar.querySelector('[data-progress-handle]');
    const cur = bar.querySelector('[data-progress-current]');
    const tot = bar.querySelector('[data-progress-total]');

    const onMeta = () => { tot.textContent = fmtTime(video.duration); };
    if (video.readyState >= 1) onMeta(); else video.addEventListener('loadedmetadata', onMeta);

    video.addEventListener('timeupdate', () => {
        if (!video.duration) return;
        const pct = (video.currentTime / video.duration) * 100;
        fill.style.width = pct + '%';
        handle.style.left = pct + '%';
        cur.textContent = fmtTime(video.currentTime);
    });

    const drag = { video, track, bar };
    const begin = (e) => {
        e.stopPropagation();
        activeProgressDrag = drag;
        bar.classList.add('is-dragging');
        progressSeek(drag, e);
    };
    track.addEventListener('mousedown', begin);
    track.addEventListener('click', (e) => e.stopPropagation());
    track.addEventListener('touchstart', begin, { passive: true });
    track.addEventListener('touchmove', (e) => {
        if (activeProgressDrag !== drag) return;
        e.preventDefault();
        progressSeek(drag, e);
    }, { passive: false });
    track.addEventListener('touchend', endProgressDrag);
    track.addEventListener('touchcancel', endProgressDrag);
}

// ── Volume / mute ─────────────────────────────────────────────────────────
const volumeBtn = document.getElementById('feedVolumeBtn');
const volumeSlider = document.getElementById('feedVolumeSlider');
const volumeIcon = volumeBtn.querySelector('.feed-icon');

function applyAudioToVideos() {
    document.querySelectorAll('.feed-slide video').forEach(v => {
        v.volume = settings.volume;
        v.muted = settings.muted;
    });
}
function updateVolumeUI() {
    volumeSlider.value = String(Math.round(settings.volume * 100));
    const muted = settings.muted || settings.volume === 0;
    const wave2 = volumeIcon.querySelector('[data-vol-wave="2"]');
    const wave3 = volumeIcon.querySelector('[data-vol-wave="3"]');
    const muteX = volumeIcon.querySelector('[data-vol-mute]');
    if (wave2) wave2.style.opacity = (!muted && settings.volume >= 0.34) ? '1' : '0';
    if (wave3) wave3.style.opacity = (!muted && settings.volume >= 0.67) ? '1' : '0';
    if (muteX) muteX.style.display = muted ? '' : 'none';
    volumeBtn.classList.toggle('is-muted', muted);
}
function setMuted(m) {
    settings.muted = !!m;
    if (!settings.muted && settings.volume === 0) { settings.volume = 0.5; }
    saveSettings();
    applyAudioToVideos();
    updateVolumeUI();
}
function toggleMute() { setMuted(!settings.muted); }
function setVolume(v) {
    settings.volume = Math.max(0, Math.min(1, v));
    settings.muted = settings.volume === 0;
    saveSettings();
    applyAudioToVideos();
    updateVolumeUI();
}

volumeBtn.addEventListener('click', () => toggleMute());
volumeSlider.addEventListener('input', (e) => setVolume(Number(e.target.value) / 100));
updateVolumeUI();

// ── Settings panel ────────────────────────────────────────────────────────
const settingsBtn = document.getElementById('feedSettingsBtn');
const settingsPanel = document.getElementById('feedSettingsPanel');
const settingsClose = document.getElementById('feedSettingsClose');
const settingsApply = document.getElementById('feedSettingsApply');
const settingsReset = document.getElementById('feedSettingsReset');
const includeInput = document.getElementById('feedIncludeTags');
const excludeInput = document.getElementById('feedExcludeTags');
const typeChecks = document.querySelectorAll('[data-type-toggle]');

function syncSettingsPanel() {
    typeChecks.forEach(cb => {
        cb.checked = settings.types.includes(cb.dataset.typeToggle);
    });
    includeInput.value = settings.includeTags;
    excludeInput.value = settings.excludeTags;
}
function openSettings() {
    syncSettingsPanel();
    settingsPanel.hidden = false;
    settingsBtn.setAttribute('aria-expanded', 'true');
    requestAnimationFrame(() => settingsPanel.classList.add('is-open'));
}
function closeSettings() {
    settingsPanel.classList.remove('is-open');
    settingsBtn.setAttribute('aria-expanded', 'false');
    setTimeout(() => { if (!settingsPanel.classList.contains('is-open')) settingsPanel.hidden = true; }, 180);
}
function toggleSettings() {
    if (settingsPanel.hidden) openSettings(); else closeSettings();
}

settingsBtn.addEventListener('click', (e) => { e.stopPropagation(); toggleSettings(); });
settingsClose.addEventListener('click', closeSettings);
document.addEventListener('click', (e) => {
    if (settingsPanel.hidden) return;
    if (settingsPanel.contains(e.target) || settingsBtn.contains(e.target)) return;
    closeSettings();
});
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !settingsPanel.hidden) closeSettings();
});

function readSettingsForm() {
    const types = [];
    typeChecks.forEach(cb => { if (cb.checked) types.push(cb.dataset.typeToggle); });
    return {
        types: types.length ? types : [...DEFAULT_SETTINGS.types],
        includeTags: includeInput.value.trim(),
        excludeTags: excludeInput.value.trim(),
    };
}
function settingsChanged(next) {
    const cur = settings;
    if (cur.includeTags !== next.includeTags) return true;
    if (cur.excludeTags !== next.excludeTags) return true;
    if (cur.types.length !== next.types.length) return true;
    const a = [...cur.types].sort().join(',');
    const b = [...next.types].sort().join(',');
    return a !== b;
}
function applySettings() {
    const next = readSettingsForm();
    const changed = settingsChanged(next);
    Object.assign(settings, next);
    saveSettings();
    closeSettings();
    if (changed) resetFeed();
}
function resetSettings() {
    settings.types = [...DEFAULT_SETTINGS.types];
    settings.includeTags = '';
    settings.excludeTags = '';
    saveSettings();
    syncSettingsPanel();
    resetFeed();
    closeSettings();
}

settingsApply.addEventListener('click', applySettings);
settingsReset.addEventListener('click', resetSettings);
[includeInput, excludeInput].forEach(inp => {
    inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); applySettings(); } });
});

// ── Feed loading ──────────────────────────────────────────────────────────
function deleteSlide(id) {
    if (!confirm('Are you sure you want to delete this file?')) return;
    fetch(`/delete/${id}`, { method: 'POST', headers: {'X-CSRFToken': csrfToken()} })
        .then(r => {
            if (!r.ok) throw new Error('fail');
            const slide = container.querySelector(`.feed-slide[data-id="${id}"]`);
            if (slide) slide.remove();
        })
        .catch(() => alert('Error deleting file.'));
}
window.deleteSlide = deleteSlide;

// ── Media windowing ───────────────────────────────────────────────────────
// Only slides near the viewport keep their media loaded. When a slide scrolls
// far away we tear its <img>/<video> source down so the browser can release the
// decoded bitmap and (for video) the buffered data + decoder. Without this,
// every file you scroll past stays resident until the tab has to be refreshed —
// exactly the slowdown this feed used to hit on long sessions. The window
// (±1.5 viewports) is wide enough that media reloads — from the HTTP cache, so
// no re-download — well before a slide scrolls back into view.
function loadSlideMedia(slide) {
    const el = slide.querySelector('.feed-media');
    if (!el || el.src) return;
    el.src = el.dataset.src;
    if (el.tagName === 'VIDEO') el.load();
}
function unloadSlideMedia(slide) {
    const el = slide.querySelector('.feed-media');
    if (!el || !el.getAttribute('src')) return;
    if (el.tagName === 'VIDEO') {
        el.pause();
        el.removeAttribute('src');
        el.load();                       // frees buffered data + decoder
        const fill = slide.querySelector('[data-progress-fill]');
        const handle = slide.querySelector('[data-progress-handle]');
        const cur = slide.querySelector('[data-progress-current]');
        if (fill) fill.style.width = '0%';
        if (handle) handle.style.left = '0%';
        if (cur) cur.textContent = '0:00';
    } else {
        el.removeAttribute('src');       // drops the decoded bitmap
    }
}

const mediaWindowObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) loadSlideMedia(e.target);
        else unloadSlideMedia(e.target);
    });
}, { root: container, rootMargin: '150% 0px', threshold: 0 });

const playObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        const v = e.target.querySelector('video');
        if (!v) return;
        if (e.isIntersecting && e.intersectionRatio > 0.6) {
            loadSlideMedia(e.target);   // ensure source is attached before play
            v.muted = settings.muted;
            v.volume = settings.volume;
            const p = v.play();
            if (p && p.catch) p.catch(() => {});
        } else {
            v.pause();
        }
    });
}, { root: container, threshold: [0, 0.6, 1] });

const sentinelObs = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) loadMore(); });
}, { root: container, rootMargin: '600px 0px' });

function buildFeedURL() {
    const url = new URL('/api/feed', location.origin);
    url.searchParams.set('seed', seed);
    url.searchParams.set('page', page);
    if (settings.types.length && settings.types.length < 3) {
        url.searchParams.set('types', settings.types.join(','));
    }
    if (settings.includeTags) url.searchParams.set('include_tags', settings.includeTags);
    if (settings.excludeTags) url.searchParams.set('exclude_tags', settings.excludeTags);
    return url;
}

function showEmptyState() {
    const empty = document.createElement('div');
    empty.className = 'feed-empty';
    empty.innerHTML = `
      <div class="empty-icon">&#128247;</div>
      <div>No media matches your filters</div>
      <div style="font-size:.78rem;">Try loosening tag filters or enabling more types.</div>
    `;
    container.appendChild(empty);
}

function resetFeed() {
    container.innerHTML = '';
    seed = Math.floor(Math.random() * 2147483647);
    page = 0;
    loading = false;
    exhausted = false;
    firstLoad = true;
    const loader = document.createElement('div');
    loader.className = 'feed-loader-slide';
    loader.innerHTML = '<div class="feed-loader"></div><div>Loading feed…</div>';
    container.appendChild(loader);
    loadMore(loader);
}

function loadMore(loaderEl) {
    if (loading || exhausted) return;
    loading = true;
    page++;
    fetch(buildFeedURL())
        .then(r => r.json())
        .then(data => {
            if (firstLoad) {
                firstLoad = false;
                if (loaderEl && loaderEl.parentNode) loaderEl.remove();
                else if (initialLoader && initialLoader.parentNode) initialLoader.remove();
                if (!data.media || data.media.length === 0) {
                    showEmptyState();
                    exhausted = true;
                    loading = false;
                    return;
                }
            }
            const oldSentinel = document.getElementById('feedSentinel');
            if (oldSentinel) oldSentinel.remove();

            (data.media || []).forEach((m, idx) => {
                const slide = buildSlide(m);
                container.appendChild(slide);
                mediaWindowObs.observe(slide);
                playObs.observe(slide);
                if (page === 1 && idx === 0) {
                    const hint = document.createElement('div');
                    hint.className = 'scroll-hint';
                    hint.textContent = 'Scroll ↓';
                    slide.appendChild(hint);
                    setTimeout(() => hint.remove(), 4000);
                }
            });

            const sentinel = document.createElement('div');
            sentinel.id = 'feedSentinel';
            sentinel.className = 'feed-loader-slide';
            if (data.has_more) {
                sentinel.innerHTML = '<div class="feed-loader"></div><div>Loading more…</div>';
            } else {
                seed = Math.floor(Math.random() * 2147483647);
                page = 0;
                sentinel.innerHTML = '<div class="feed-loader"></div><div>Reshuffling…</div>';
            }
            container.appendChild(sentinel);
            sentinelObs.observe(sentinel);

            loading = false;
        })
        .catch((err) => {
            console.error('feed load failed', err);
            loading = false;
        });
}

window.addEventListener('resize', () => {
    const h = (window.innerHeight - 58) + 'px';
    container.style.height = h;
    document.querySelectorAll('.feed-slide').forEach(s => {
        s.style.height = h;
        s.style.minHeight = h;
    });
});
container.style.height = (window.innerHeight - 58) + 'px';

syncSettingsPanel();
loadMore();

document.addEventListener('keydown', e => {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
    if (!settingsPanel.hidden) return;
    const slides = [...container.querySelectorAll('.feed-slide')];
    if (!slides.length) return;
    const top = container.scrollTop;
    const slideH = slides[0].clientHeight || 1;
    const idx = Math.round(top / slideH);
    let target = idx;
    if (e.key === 'ArrowDown' || e.key === 'j') target = Math.min(idx + 1, slides.length - 1);
    else if (e.key === 'ArrowUp' || e.key === 'k') target = Math.max(idx - 1, 0);
    else if (e.key === 'm') { toggleMute(); return; }
    else return;
    e.preventDefault();
    slides[target].scrollIntoView({ behavior: 'smooth', block: 'start' });
});
