// Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active from all tabs
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
            
            // Add active to clicked tab
            this.classList.add('active');
            const tabName = this.dataset.tab;
            document.getElementById(tabName + '-content').style.display = 'block';
        });
    });

    // Filter buttons
    document.querySelectorAll('.filter-group .btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-group .btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // In production, this would filter the list
            const filter = this.textContent.trim();
            console.log('Filtering by:', filter);
        });
    });

    // Approve candidatura
    function aprovarCandidatura(id) {
        if (confirm('Tem certeza que deseja aprovar esta candidatura?')) {
            // In production, make AJAX call to approve
            alert('Candidatura aprovada com sucesso!');
            window.location.reload();
        }
    }

    // Reject candidatura
    function rejeitarCandidatura(id) {
        if (confirm('Tem certeza que deseja rejeitar esta candidatura?')) {
            // In production, make AJAX call to reject
            alert('Candidatura rejeitada.');
            window.location.reload();
        }
    }

    // Add animation to list items
    document.addEventListener('DOMContentLoaded', function() {
        const items = document.querySelectorAll('.candidato-item');
        items.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(10px)';
            setTimeout(() => {
                item.style.transition = 'all 0.3s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 30);
        });
    });