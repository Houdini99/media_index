let visibleCount = window.MEDIA_INDEX.totalTags;
  const totalCount = window.MEDIA_INDEX.totalTags;

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
          window.location.href = window.MEDIA_INDEX.indexUrl + '?search=' + encodeURIComponent(tag);
      });
  });
