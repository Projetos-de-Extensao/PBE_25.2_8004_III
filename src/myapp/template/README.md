# Sistema de Monitoria - Templates HTML/CSS

Este diretório contém todos os templates HTML e arquivos estáticos (CSS, JS) para o Sistema de Monitoria.

## Estrutura de Arquivos

```
template/
├── base.html                    # Template base com navbar e footer
├── home.html                    # Página inicial
├── login.html                   # Página de login
├── cadastro_aluno.html         # Cadastro de aluno
├── cadastro_professor.html     # Cadastro de professor
├── cadastro_vaga.html          # Cadastro de vaga de monitoria
├── lista_vagas.html            # Listagem de vagas
├── painel_monitor.html         # Painel do monitor
├── painel_coordenador.html     # Painel administrativo do coordenador
├── dashboard.html              # Dashboard com métricas
└── static/
    └── css/
        └── style.css           # Estilos globais
```

## Templates Criados

### 1. **base.html**
Template base com estrutura comum (navbar, footer, imports CSS/JS)

### 2. **home.html**
- Hero section com boas-vindas
- Cards de features
- Estatísticas rápidas
- Call-to-action para cadastro

### 3. **login.html**
- Formulário de login
- Seletor de tipo de usuário (Aluno, Professor, Coordenador)
- Link para cadastro

### 4. **cadastro_aluno.html**
- Formulário completo de cadastro
- Campos: nome, matrícula, email, telefone, CR geral, CR disciplina, curso, senha

### 5. **cadastro_professor.html**
- Formulário de cadastro de professor
- Opção para cadastro como coordenador
- Campos: nome, matrícula, CPF, email, telefone, senha

### 6. **cadastro_vaga.html**
- Formulário para criação de vagas
- Campos: título, disciplina, pré-requisitos, prazo, status

### 7. **lista_vagas.html**
- Listagem de todas as vagas
- Filtros de busca e status
- Cards com informações da vaga
- Botões de ação (ver detalhes, candidatar-se, editar)

### 8. **painel_monitor.html**
- Sistema de tabs (Atividades, Registros, Horários, Histórico)
- Formulário para registrar monitoria
- Gerenciamento de disponibilidade
- Histórico de monitorias

### 9. **painel_coordenador.html**
- Tabs para gestão (Candidaturas, Vagas, Monitores, Validações)
- Lista de candidaturas pendentes
- Gerenciamento de vagas
- Lista de monitores ativos
- Validação de registros

### 10. **dashboard.html**
- Métricas principais (cards de estatísticas)
- Gráficos (placeholders para Chart.js)
- Feed de atividades recentes
- Top monitores do mês

## Estilos CSS

### Características do Design

- **Cores principais:**
  - Primary: #2563eb (azul)
  - Secondary: #10b981 (verde)
  - Danger: #ef4444 (vermelho)
  - Warning: #f59e0b (laranja)

- **Componentes:**
  - Navbar responsiva
  - Cards com sombras
  - Formulários estilizados
  - Botões com hover effects
  - Tabelas responsivas
  - Badges de status
  - Grid layouts
  - Alerts

- **Responsividade:**
  - Mobile-first approach
  - Breakpoint em 768px
  - Grid adaptativo

## Configuração no Django

### 1. Configurar TEMPLATES em settings.py

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'myapp/template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### 2. Configurar STATIC_URL em settings.py

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myapp/template/static'),
]
```

### 3. URLs de Exemplo (urls.py)

```python
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/professor/', views.cadastro_professor, name='cadastro_professor'),
    path('vagas/', views.lista_vagas, name='lista_vagas'),
    path('vagas/cadastrar/', views.cadastro_vaga, name='cadastro_vaga'),
    path('vagas/<int:vaga_id>/', views.detalhes_vaga, name='detalhes_vaga'),
    path('vagas/<int:vaga_id>/candidatar/', views.candidatar_vaga, name='candidatar_vaga'),
    path('monitor/painel/', views.painel_monitor, name='painel_monitor'),
    path('monitor/registrar/', views.registrar_monitoria, name='registrar_monitoria'),
    path('coordenador/painel/', views.painel_coordenador, name='painel_coordenador'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

## Próximos Passos

### Implementações Necessárias:

1. **Autenticação:**
   - Implementar sistema de autenticação customizado
   - Gerenciar sessões de usuário
   - Middleware para verificar tipo de usuário

2. **Permissões:**
   - Decorators para restringir acesso por tipo de usuário
   - Validação de permissões nas views

3. **JavaScript:**
   - Validação de formulários no client-side
   - Máscaras para CPF, telefone
   - Confirmações de ações
   - AJAX para aprovação/rejeição de candidaturas

4. **Gráficos:**
   - Integrar Chart.js para dashboard
   - Implementar gráficos de barras, linhas e pizza

5. **Funcionalidades Adicionais:**
   - Upload de documentos para candidaturas
   - Sistema de notificações
   - Exportação de relatórios (PDF, Excel)
   - Busca avançada com filtros

## Como Testar

1. Execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. Crie um superusuário (se necessário):
```bash
python manage.py createsuperuser
```

3. Inicie o servidor:
```bash
python manage.py runserver
```

4. Acesse no navegador:
```
http://localhost:8000/
```

## Observações

- Os templates usam `{% load static %}` para carregar arquivos CSS/JS
- Alguns campos comentados nas views precisam de implementação de autenticação
- Os erros de import do Django/DRF no linter são esperados (dependências não instaladas no ambiente de análise)
- Templates são responsivos e funcionam em dispositivos móveis

## Suporte

Para dúvidas ou problemas, consulte a documentação do Django em https://docs.djangoproject.com/
