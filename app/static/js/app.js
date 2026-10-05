const modal = document.getElementById('upload-modal');
const uploadTrigger = document.getElementById('upload-trigger');
const closeButton = document.getElementById('close-upload');
const uploadForm = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const selectedFile = document.getElementById('selected-file');
const uploadError = document.getElementById('upload-error');
const searchInput = document.getElementById('book-search');

const formatFileSize = (bytes) => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

if (fileInput) {
  fileInput.addEventListener('change', () => {
    const [file] = fileInput.files;
    uploadError.classList.add('hidden');

    if (!file) {
      selectedFile.classList.add('hidden');
      selectedFile.textContent = '';
      return;
    }

    selectedFile.textContent = `${file.name} · ${formatFileSize(file.size)}`;
    selectedFile.classList.remove('hidden');
  });
}

if (uploadTrigger) {
  uploadTrigger.addEventListener('click', () => {
    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');
  });
}

if (closeButton) {
  closeButton.addEventListener('click', () => {
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
  });
}

if (uploadForm) {
  uploadForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    uploadError.classList.add('hidden');

    if (!fileInput.files.length) {
      uploadError.textContent = 'Select a file before uploading.';
      uploadError.classList.remove('hidden');
      return;
    }

    const formData = new FormData(uploadForm);
    const response = await fetch('/api/books', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      window.location.reload();
      return;
    }

    const result = await response.json().catch(() => ({}));
    uploadError.textContent = result.error || 'The file could not be uploaded.';
    uploadError.classList.remove('hidden');
  });
}

if (searchInput) {
  searchInput.addEventListener('input', (event) => {
    const term = event.target.value.trim().toLowerCase();
    const cards = document.querySelectorAll('.book-card');
    cards.forEach((card) => {
      const title = (card.dataset.title || '').toLowerCase();
      const author = (card.dataset.author || '').toLowerCase();
      const series = (card.dataset.series || '').toLowerCase();
      const matches = !term || title.includes(term) || author.includes(term) || series.includes(term);
      card.style.display = matches ? '' : 'none';
    });
  });
}

const deleteButton = document.querySelector('[data-delete-id]');
if (deleteButton) {
  deleteButton.addEventListener('click', async () => {
    const shouldDelete = window.confirm('Remove the book from the library only, or remove the book and file?');
    const url = `/api/books/${deleteButton.dataset.deleteId}?delete_file=${shouldDelete ? 'true' : 'false'}`;
    const response = await fetch(url, { method: 'DELETE' });
    if (response.ok) {
      window.location.href = '/';
    }
  });
}
