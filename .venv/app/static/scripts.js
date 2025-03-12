// Load more photos (example for pagination)
document.addEventListener('DOMContentLoaded', function () {
    const loadMoreButton = document.getElementById('load-more');
    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', function () {
            let page = parseInt(this.getAttribute('data-page')) || 1;
            page++;
            fetch(`/photo?page=${page}`)
                .then(response => response.text())
                .then(html => {
                    document.getElementById('photo-list').innerHTML += html;
                    this.setAttribute('data-page', page);
                });
        });
    }

    // Search functionality (example)
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = this.value.toLowerCase();
            const items = document.querySelectorAll('.photo-item');
            items.forEach(item => {
                const title = item.querySelector('.photo-title').textContent.toLowerCase();
                if (title.includes(query)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
});