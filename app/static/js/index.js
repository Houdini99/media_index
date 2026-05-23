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
            ['type','search','exclude_tags','hide_ai','private_only'].forEach(k => {
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
            const dlName = d.download_name || filename;
            dl.href = '/media/' + filename;
            dl.setAttribute('download', dlName);
            dl.textContent = '↓ ' + dlName;

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
