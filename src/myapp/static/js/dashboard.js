/* configuração padrão do Chart.js para tema escuro */
Chart.defaults.color = '#9ca3af';
Chart.defaults.borderColor = '#374151';

/* gráfico de barras - presença dos alunos */
const presencaCtx = document.getElementById('presencaChart');
if (presencaCtx) {
    // Pegar dados do contexto Django
    const presencaLabels = JSON.parse(document.getElementById('presenca-labels-data')?.textContent || '["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]');
    const presencaData = JSON.parse(document.getElementById('presenca-data-data')?.textContent || '[12, 35, 42, 38, 45, 40, 18]');
    
    new Chart(presencaCtx, {
        type: 'bar',
        data: {
            labels: presencaLabels,
            datasets: [{
                label: 'Alunos Presentes',
                data: presencaData,
                backgroundColor: 'rgba(91, 155, 213, 0.8)',
                borderColor: 'rgba(91, 155, 213, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(42, 42, 42, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#9ca3af',
                    borderColor: '#374151',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#9ca3af',
                        stepSize: 1
                    },
                    grid: {
                        color: '#374151'
                    }
                },
                x: {
                    ticks: {
                        color: '#9ca3af'
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/* gráfico de pizza - distribuição por disciplina */
const disciplinasCtx = document.getElementById('disciplinasChart');
if (disciplinasCtx) {
    // Pegar dados do contexto Django
    const disciplinasLabels = JSON.parse(document.getElementById('disciplinas-labels-data')?.textContent || '["Cálculo I", "Programação", "Física II"]');
    const disciplinasData = JSON.parse(document.getElementById('disciplinas-data-data')?.textContent || '[28, 22, 18]');
    
    new Chart(disciplinasCtx, {
        type: 'pie',
        data: {
            labels: disciplinasLabels,
            datasets: [{
                data: disciplinasData,
                backgroundColor: [
                    'rgba(91, 155, 213, 0.8)',
                    'rgba(112, 196, 112, 0.8)',
                    'rgba(255, 165, 0, 0.8)',
                    'rgba(231, 76, 60, 0.8)',
                    'rgba(155, 89, 182, 0.8)',
                    'rgba(149, 165, 166, 0.8)'
                ],
                borderColor: '#2a2a2a',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#9ca3af',
                        padding: 15,
                        font: {
                            size: 12
                        },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(42, 42, 42, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#9ca3af',
                    borderColor: '#374151',
                    borderWidth: 1,
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Função para ver detalhes de uma monitoria
function verDetalhesMonitoria(id) {
    // Redireciona para a página de detalhes da monitoria
    window.location.href = `/detalhes_monitoria/${id}/`;
}
