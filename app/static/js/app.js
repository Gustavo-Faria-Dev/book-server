const modal = document.getElementById('upload-modal');
const closeButton = document.getElementById('close-upload');
const uploadForm = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const selectedFile = document.getElementById('selected-file');
const uploadError = document.getElementById('upload-error');
const searchInput = document.getElementById('book-search');
const uploadSubmit = document.getElementById('upload-submit');
const dropzone = document.querySelector('.upload-dropzone');
const noResults = document.getElementById('no-results');
const clearFilters = document.getElementById('clear-filters');
const filters = document.querySelectorAll('[data-filter]');
let activeFilter = 'all';

const formatFileSize = (bytes) => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const updateSelectedFile = () => {
  if (!fileInput) return;
    const [file] = fileInput.files;
    uploadError.classList.add('hidden');

    if (!file) {
      selectedFile.classList.add('hidden');
      selectedFile.textContent = '';
      return;
    }

    selectedFile.textContent = `${file.name} · ${formatFileSize(file.size)}`;
    selectedFile.classList.remove('hidden');
};

if (fileInput) {
  fileInput.addEventListener('change', updateSelectedFile);
}

if (dropzone) {
  ['dragenter', 'dragover'].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.add('drag-over');
    });
  });
  ['dragleave', 'drop'].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.remove('drag-over');
    });
  });
  dropzone.addEventListener('drop', (event) => {
    const [file] = event.dataTransfer.files;
    if (!file) return;
    const transfer = new DataTransfer();
    transfer.items.add(file);
    fileInput.files = transfer.files;
    updateSelectedFile();
  });
}

const openModal = () => {
  if (!modal) return;
    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');
    fileInput?.focus();
};

const closeModal = () => {
  if (!modal) return;
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
};

document.querySelectorAll('#upload-trigger, [data-open-upload]').forEach((button) => {
  button.addEventListener('click', openModal);
});
closeButton?.addEventListener('click', closeModal);
modal?.addEventListener('click', (event) => {
  if (event.target === modal) closeModal();
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && modal && !modal.classList.contains('hidden')) closeModal();
});

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
    uploadSubmit.disabled = true;
    uploadSubmit.textContent = 'Adding...';
    try {
      const response = await fetch('/api/books', { method: 'POST', body: formData });
      if (response.ok) {
        window.location.reload();
        return;
      }
      const result = await response.json().catch(() => ({}));
      uploadError.textContent = result.error || 'The file could not be uploaded.';
      uploadError.classList.remove('hidden');
    } catch {
      uploadError.textContent = 'Connection failed. Please try again.';
      uploadError.classList.remove('hidden');
    } finally {
      uploadSubmit.disabled = false;
      uploadSubmit.textContent = 'Add book';
    }
  });
}

const applyFilters = () => {
  const term = (searchInput?.value || '').trim().toLowerCase();
  const cards = document.querySelectorAll('.book-card');
  let visibleCount = 0;
  cards.forEach((card) => {
    const title = (card.dataset.title || '').toLowerCase();
    const author = (card.dataset.author || '').toLowerCase();
    const series = (card.dataset.series || '').toLowerCase();
    const format = (card.dataset.format || '').toLowerCase();
    const matchesSearch = !term || title.includes(term) || author.includes(term) || series.includes(term);
    const matchesFilter = activeFilter === 'all'
      || activeFilter === format
      || (activeFilter === 'authors' && author)
      || (activeFilter === 'series' && series);
    const visible = matchesSearch && matchesFilter;
    card.style.display = visible ? '' : 'none';
    if (visible) visibleCount += 1;
  });
  noResults?.classList.toggle('hidden', visibleCount > 0 || cards.length === 0);
};

if (searchInput) {
  searchInput.addEventListener('input', applyFilters);
}

filters.forEach((filter) => {
  filter.addEventListener('click', () => {
    activeFilter = filter.dataset.filter;
    filters.forEach((item) => {
      const selected = item === filter;
      item.classList.toggle('active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    applyFilters();
  });
});

clearFilters?.addEventListener('click', () => {
  if (searchInput) searchInput.value = '';
  activeFilter = 'all';
  filters.forEach((filter) => {
    const selected = filter.dataset.filter === 'all';
    filter.classList.toggle('active', selected);
    filter.setAttribute('aria-pressed', String(selected));
  });
  applyFilters();
});

if (searchInput) {
  searchInput.addEventListener('search', applyFilters);
}

if (searchInput?.value) {
  applyFilters();
}

const deleteButton = document.querySelector('[data-delete-id]');
if (deleteButton) {
  deleteButton.addEventListener('click', async () => {
    const shouldDelete = window.confirm('Delete the book file from your device too? Cancel keeps the file and removes only the library entry.');
    const url = `/api/books/${deleteButton.dataset.deleteId}?delete_file=${shouldDelete ? 'true' : 'false'}`;
    const response = await fetch(url, { method: 'DELETE' });
    if (response.ok) {
      window.location.href = '/';
    } else {
      window.alert('The book could not be deleted. Please try again.');
    }
  });
}
