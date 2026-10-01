const modal = document.getElementById('upload-modal');
const uploadTrigger = document.getElementById('upload-trigger');
const closeButton = document.getElementById('close-upload');
const uploadForm = document.getElementById('upload-form');
const searchInput = document.getElementById('book-search');

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
    const formData = new FormData(uploadForm);
    const response = await fetch('/api/books', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      window.location.reload();
    }
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
