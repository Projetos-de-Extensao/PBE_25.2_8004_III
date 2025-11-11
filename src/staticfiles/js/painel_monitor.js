// Tab switching
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(tc => tc.classList.remove('active'));
            
            tab.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // Horário selection
    const horarioCards = document.querySelectorAll('.horario-card');
    horarioCards.forEach(card => {
        card.addEventListener('click', () => {
            card.classList.toggle('selected');
        });
    });