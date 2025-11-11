// Search functionality
    const searchInput = document.getElementById('search');
    const statusFilter = document.getElementById('status-filter');
    const vagasCards = document.querySelectorAll('.vaga-card');

    function filterVagas() {
        const searchTerm = searchInput.value.toLowerCase();
        const statusValue = statusFilter.value;

        vagasCards.forEach(card => {
            const title = card.querySelector('.vaga-title').textContent.toLowerCase();
            const disciplina = card.querySelector('.vaga-disciplina').textContent.toLowerCase();
            const status = card.getAttribute('data-status');

            const matchesSearch = title.includes(searchTerm) || disciplina.includes(searchTerm);
            const matchesStatus = !statusValue || status === statusValue;

            if (matchesSearch && matchesStatus) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterVagas);
    statusFilter.addEventListener('change', filterVagas);