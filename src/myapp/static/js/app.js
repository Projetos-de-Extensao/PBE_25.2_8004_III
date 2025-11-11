// Funções JavaScript para o Sistema de Monitoria

// ==================== VALIDAÇÃO DE FORMULÁRIOS ====================

// Validar CPF
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
    
    let soma = 0;
    let resto;
    
    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i-1, i)) * (11 - i);
    }
    
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(9, 10))) return false;
    
    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i-1, i)) * (12 - i);
    }
    
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(10, 11))) return false;
    
    return true;
}

// Validar Email
function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validar senhas iguais
function validarSenhas(senha1, senha2) {
    return senha1 === senha2 && senha1.length >= 6;
}

// ==================== MÁSCARAS DE INPUT ====================

// Máscara de CPF (000.000.000-00)
function mascaraCPF(input) {
    let valor = input.value.replace(/\D/g, '');
    valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
    valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
    valor = valor.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    input.value = valor;
}

// Máscara de Telefone ((00) 00000-0000)
function mascaraTelefone(input) {
    let valor = input.value.replace(/\D/g, '');
    valor = valor.replace(/^(\d{2})(\d)/g, '($1) $2');
    valor = valor.replace(/(\d)(\d{4})$/, '$1-$2');
    input.value = valor;
}

// Aplicar máscaras automaticamente
document.addEventListener('DOMContentLoaded', function() {
    // Máscara CPF
    const inputsCPF = document.querySelectorAll('input[name="cpf"]');
    inputsCPF.forEach(input => {
        input.addEventListener('input', function() {
            mascaraCPF(this);
        });
    });
    
    // Máscara Telefone
    const inputsTelefone = document.querySelectorAll('input[name="telefone"]');
    inputsTelefone.forEach(input => {
        input.addEventListener('input', function() {
            mascaraTelefone(this);
        });
    });
});

// ==================== VALIDAÇÃO DE FORMULÁRIOS ====================

// Validar formulário de cadastro de aluno
function validarCadastroAluno(form) {
    const senha = form.querySelector('input[name="senha"]').value;
    const confirmarSenha = form.querySelector('input[name="confirmar_senha"]').value;
    
    if (!validarSenhas(senha, confirmarSenha)) {
        alert('As senhas não coincidem ou são muito curtas (mínimo 6 caracteres)!');
        return false;
    }
    
    const email = form.querySelector('input[name="email"]').value;
    if (!validarEmail(email)) {
        alert('Email inválido!');
        return false;
    }
    
    return true;
}

// Validar formulário de cadastro de professor
function validarCadastroProfessor(form) {
    const cpf = form.querySelector('input[name="cpf"]').value;
    if (!validarCPF(cpf)) {
        alert('CPF inválido!');
        return false;
    }
    
    const senha = form.querySelector('input[name="senha"]').value;
    const confirmarSenha = form.querySelector('input[name="confirmar_senha"]').value;
    
    if (!validarSenhas(senha, confirmarSenha)) {
        alert('As senhas não coincidem ou são muito curtas (mínimo 6 caracteres)!');
        return false;
    }
    
    const email = form.querySelector('input[name="email"]').value;
    if (!validarEmail(email)) {
        alert('Email inválido!');
        return false;
    }
    
    return true;
}

// ==================== CONFIRMAÇÕES ====================

// Confirmar exclusão
function confirmarExclusao(mensagem = 'Tem certeza que deseja excluir?') {
    return confirm(mensagem);
}

// Confirmar ação
function confirmarAcao(mensagem) {
    return confirm(mensagem);
}

// ==================== UTILITÁRIOS ====================

// Mostrar/Ocultar senha
function toggleSenha(inputId, buttonId) {
    const input = document.getElementById(inputId);
    const button = document.getElementById(buttonId);
    
    if (input.type === 'password') {
        input.type = 'text';
        button.textContent = '🙈';
    } else {
        input.type = 'password';
        button.textContent = '👁️';
    }
}

// Calcular CR automaticamente (se necessário)
function calcularCR(notas) {
    if (notas.length === 0) return 0;
    const soma = notas.reduce((acc, nota) => acc + nota, 0);
    return (soma / notas.length).toFixed(2);
}

// Formatar data para exibição (DD/MM/YYYY)
function formatarData(data) {
    const d = new Date(data);
    const dia = String(d.getDate()).padStart(2, '0');
    const mes = String(d.getMonth() + 1).padStart(2, '0');
    const ano = d.getFullYear();
    return `${dia}/${mes}/${ano}`;
}

// Formatar hora (HH:MM)
function formatarHora(hora) {
    return hora.substring(0, 5);
}

// ==================== AJAX HELPERS ====================

// Função genérica para requisições AJAX
async function fazerRequisicao(url, metodo = 'GET', dados = null) {
    const opcoes = {
        method: metodo,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };
    
    if (dados && metodo !== 'GET') {
        opcoes.body = JSON.stringify(dados);
    }
    
    try {
        const response = await fetch(url, opcoes);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

// Obter CSRF token dos cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ==================== NOTIFICAÇÕES ====================

// Mostrar notificação (toast)
function mostrarNotificacao(mensagem, tipo = 'success') {
    const container = document.getElementById('notifications-container') || criarContainerNotificacoes();
    
    const notificacao = document.createElement('div');
    notificacao.className = `alert alert-${tipo}`;
    notificacao.style.cssText = 'margin-bottom: 1rem; animation: slideIn 0.3s ease-out;';
    notificacao.textContent = mensagem;
    
    container.appendChild(notificacao);
    
    setTimeout(() => {
        notificacao.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notificacao.remove(), 300);
    }, 3000);
}

function criarContainerNotificacoes() {
    const container = document.createElement('div');
    container.id = 'notifications-container';
    container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    document.body.appendChild(container);
    return container;
}

// ==================== FILTROS E BUSCA ====================

// Filtrar tabela
function filtrarTabela(inputId, tabelaId) {
    const input = document.getElementById(inputId);
    const tabela = document.getElementById(tabelaId);
    const filtro = input.value.toUpperCase();
    const linhas = tabela.getElementsByTagName('tr');
    
    for (let i = 1; i < linhas.length; i++) {
        const linha = linhas[i];
        const textoLinha = linha.textContent || linha.innerText;
        
        if (textoLinha.toUpperCase().indexOf(filtro) > -1) {
            linha.style.display = '';
        } else {
            linha.style.display = 'none';
        }
    }
}

// Debounce para otimizar buscas
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== VALIDAÇÃO DE DATAS ====================

// Verificar se data é futura
function isDataFutura(data) {
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    const dataComparacao = new Date(data);
    dataComparacao.setHours(0, 0, 0, 0);
    return dataComparacao > hoje;
}

// Verificar se data é passada
function isDataPassada(data) {
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    const dataComparacao = new Date(data);
    dataComparacao.setHours(0, 0, 0, 0);
    return dataComparacao < hoje;
}

// ==================== ANIMAÇÕES CSS ====================

// Adicionar animações via CSS
const styles = `
@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOut {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);

// ==================== EXPORTAÇÕES ====================

// Se estiver usando módulos ES6, exporte as funções necessárias
// export { validarCPF, validarEmail, mascaraCPF, mascaraTelefone, mostrarNotificacao, ... };
