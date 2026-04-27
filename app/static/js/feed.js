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
