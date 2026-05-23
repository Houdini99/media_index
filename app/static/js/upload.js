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

            const privacyLabel = document.createElement('label');
            privacyLabel.className = 'privacy-toggle';
            privacyLabel.title = 'Only you will see this file';
            const privacyInput = document.createElement('input');
            privacyInput.type = 'checkbox';
            privacyInput.name = 'private_' + i;
            privacyInput.value = '1';
            const privacyText = document.createElement('span');
            privacyText.textContent = 'Private (only visible to you)';
            privacyLabel.appendChild(privacyInput);
            privacyLabel.appendChild(privacyText);

            details.appendChild(fname);
            details.appendChild(tagInput);
            details.appendChild(privacyLabel);
            div.appendChild(media);
            div.appendChild(details);
            previewsDiv.appendChild(div);
        });
    });
});
