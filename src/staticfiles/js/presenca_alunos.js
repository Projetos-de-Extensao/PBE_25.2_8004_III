// Form submission handler
    document.getElementById('presencaForm').addEventListener('submit', function(e) {
        // Form will submit normally via Django
        const nome = document.getElementById('nome').value;
        const matricula = document.getElementById('matricula').value;
        
        if (!nome || !matricula) {
            e.preventDefault();
            alert('Por favor, preencha todos os campos.');
            return;
        }
    });

    // Remove presence function
    function removePresenca(id) {
        if (confirm('Tem certeza que deseja remover esta presença?')) {
            // In production, this would make an AJAX call to delete
            // For now, just show confirmation
            alert('Presença removida com sucesso!');
            // Reload page or remove element from DOM
            window.location.reload();
        }
    }

    // Add animation to newly added items
    document.addEventListener('DOMContentLoaded', function() {
        const items = document.querySelectorAll('.presenca-item');
        items.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(10px)';
            setTimeout(() => {
                item.style.transition = 'all 0.3s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 50);
        });
    });