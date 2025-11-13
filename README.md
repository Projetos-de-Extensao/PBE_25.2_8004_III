# Sistema de Monitoria IBMEC

**Código da Disciplina**: IBM8936<br>
**Projeto**: Back-End 2025.2<br>

<div align="center">
  <h3>🎓 Plataforma de Gestão de Monitoria Acadêmica</h3>
</div>

---

## 📋 Sobre o Projeto

O **Sistema de Monitoria IBMEC** é uma plataforma web completa voltada para a gestão de monitoria acadêmica. O sistema centraliza todas as vagas de monitoria da faculdade, permitindo:

- **Alunos**: Criar perfil, buscar vagas, candidatar-se e acompanhar status em tempo real
- **Professores**: Aprovar ou rejeitar candidaturas de monitoria
- **Coordenadores**: Criar e gerenciar vagas, aprovar candidaturas, acessar dashboard completo
- **Monitores TEA**: Registrar horas trabalhadas e submeter relatórios de monitoria
- **Casa (Admin)**: Gerenciar coordenadores e ter controle total do sistema

### 🎯 Objetivos
- Facilitar o acesso às oportunidades de monitoria
- Aumentar a participação dos alunos no programa
- Automatizar o processo de seleção e aprovação
- Centralizar a gestão de vagas e candidaturas
- Registrar e acompanhar horas de monitoria (Monitor TEA)

---

## 👥 Equipe

| Nome | Papel |
|------|-------|
| João Victor Carvalho | Desenvolvedor Full Stack |
| João Mariano | Desenvolvedor Back-End |
| João Vitor Donda | Desenvolvedor Front-End |
| Sarah Ferrari | Desenvolvedora Full Stack |
| Caique Rechuan | Desenvolvedor Back-End |

---

## 🛠️ Tecnologias Utilizadas

### Back-End
- **Python 3.11** - Linguagem de programação
- **Django 5.2.8** - Framework web
- **Django REST Framework** - API REST
- **SQLite** - Banco de dados (desenvolvimento)
- **bcrypt** - Criptografia de senhas

### Front-End
- **HTML5** - Estrutura
- **CSS3** - Estilização
- **JavaScript** - Interatividade
- **Montserrat** - Tipografia customizada

### Ferramentas
- **Git & GitHub** - Controle de versão
- **Visual Studio Code** - IDE
- **MkDocs** - Documentação

---

## 📊 Arquitetura do Sistema

### Modelos Principais
- **Usuario** (abstrato): Aluno, Professor, Coordenador, Casa
- **Monitor** e **MonitorTEA**: Monitores voluntários e remunerados
- **VagaMonitoria**: Vagas de monitoria
- **Candidatura**: Candidaturas de alunos
- **RegistroMonitoria**: Registro de horas (Monitor TEA)
- **Disciplina**: Disciplinas acadêmicas

### Permissões por Perfil

| Funcionalidade | Aluno | Professor | Coordenador | Casa |
|----------------|-------|-----------|-------------|------|
| Candidatar-se a vagas | ✅ | ❌ | ❌ | ❌ |
| Aprovar/Rejeitar candidaturas | ❌ | ✅ | ✅ | ✅ |
| Criar vagas | ❌ | ❌ | ✅ | ✅ |
| Acessar dashboard | ❌ | ❌ | ✅ | ✅ |
| Registrar monitoria | Monitor TEA | ❌ | ❌ | ❌ |
| Gerenciar coordenadores | ❌ | ❌ | ❌ | ✅ |

---

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/Projetos-de-Extensao/PBE_25.2_8004_III.git
cd PBE_25.2_8004_III
```

### Passo 2: Criar Ambiente Virtual
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows CMD
python -m venv venv
venv\Scripts\activate.bat

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Banco de Dados
```bash
cd src
python manage.py migrate
```

### Passo 5: Coletar Arquivos Estáticos
```bash
python manage.py collectstatic --noinput
```

### Passo 6: Criar Superusuário (Opcional)
```bash
python manage.py createsuperuser
```

### Passo 7: Executar o Servidor
```bash
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000**

---

## 🧪 Como Rodar os Testes

### Executar Todos os Testes
```bash
cd src
python manage.py test myapp
```

### Executar Testes Específicos
```bash
# Testar apenas models
python manage.py test myapp.tests.TestModels

# Testar apenas views
python manage.py test myapp.tests.TestViews

# Testar um método específico
python manage.py test myapp.tests.TestModels.test_aluno_creation
```

### Executar com Verbosidade
```bash
python manage.py test myapp --verbosity=2
```

### Executar com Cobertura de Código
```bash
# Instalar coverage
pip install coverage

# Executar testes com coverage
coverage run --source='.' manage.py test myapp

# Gerar relatório
coverage report

# Gerar relatório HTML
coverage html
# Abra htmlcov/index.html no navegador
```

### Estrutura dos Testes
```
src/myapp/tests.py
├── TestModels - Testes de modelos
│   ├── test_aluno_creation
│   ├── test_candidatura_validation
│   ├── test_vaga_creation
│   └── ...
├── TestViews - Testes de views
│   ├── test_login_view
│   ├── test_cadastro_aluno
│   ├── test_candidatar_vaga
│   └── ...
└── TestAPI - Testes de API
    ├── test_api_vagas_list
    ├── test_api_candidaturas
    └── ...
```

---

## 🔌 Como Usar a API REST

### Base URL
```
http://127.0.0.1:8000/api/
```

### Autenticação
A API utiliza **Session Authentication**. Para acessar endpoints protegidos, primeiro faça login através da interface web ou obtenha um token de sessão.

---

### 📍 Endpoints Disponíveis

#### **1. Vagas de Monitoria**

##### Listar Todas as Vagas
```http
GET /api/vagas/
```

**Resposta (200 OK):**
```json
[
  {
    "id": 1,
    "titulo": "Monitor de Cálculo I",
    "disciplina": {
      "id": 1,
      "nome": "Cálculo I",
      "codigo": "MAT101"
    },
    "tipo_monitoria": "Monitor",
    "status": "Aberta",
    "prazo_inscricao": "2025-12-31",
    "pre_requisitos": "CR mínimo 8.0 em Cálculo I",
    "coordenador": {
      "nome": "Prof. João Silva",
      "cpf": "123.456.789-00"
    }
  }
]
```

##### Obter Vaga Específica
```http
GET /api/vagas/{id}/
```

##### Criar Nova Vaga (Coordenador/Casa)
```http
POST /api/vagas/
Content-Type: application/json

{
  "titulo": "Monitor de Programação",
  "disciplina_id": 2,
  "tipo_monitoria": "MonitorTEA",
  "prazo_inscricao": "2025-12-31",
  "pre_requisitos": "CR geral ≥ 7.0, CR disciplina ≥ 8.0"
}
```

**Resposta (201 Created):**
```json
{
  "id": 5,
  "titulo": "Monitor de Programação",
  "status": "Aberta",
  "message": "Vaga criada com sucesso"
}
```

##### Atualizar Vaga (Coordenador/Casa)
```http
PUT /api/vagas/{id}/
Content-Type: application/json

{
  "titulo": "Monitor de Programação I",
  "status": "Fechada"
}
```

##### Deletar Vaga (Coordenador/Casa)
```http
DELETE /api/vagas/{id}/
```

---

#### **2. Candidaturas**

##### Listar Candidaturas do Aluno Logado
```http
GET /api/candidaturas/
```

**Resposta (200 OK):**
```json
[
  {
    "id": 10,
    "vaga": {
      "id": 1,
      "titulo": "Monitor de Cálculo I",
      "disciplina": "Cálculo I"
    },
    "status": "Pendente",
    "data_candidatura": "2025-11-10",
    "cr_disciplina": 8.5,
    "documentos": "Histórico escolar anexado"
  }
]
```

##### Criar Candidatura
```http
POST /api/candidaturas/
Content-Type: application/json

{
  "vaga_id": 1,
  "cr_disciplina": 8.5,
  "documentos": "Histórico escolar e carta de motivação"
}
```

**Resposta (201 Created):**
```json
{
  "id": 15,
  "message": "Candidatura enviada com sucesso",
  "status": "Pendente"
}
```

**Possíveis Erros:**
```json
// CR geral insuficiente
{
  "error": "CR geral insuficiente. Mínimo: 7.0"
}

// CR disciplina insuficiente
{
  "error": "CR na disciplina insuficiente. Mínimo: 8.0"
}

// Candidatura duplicada
{
  "error": "Você já possui uma candidatura para esta vaga"
}
```

##### Cancelar Candidatura
```http
DELETE /api/candidaturas/{id}/
```

---

#### **3. Disciplinas**

##### Listar Todas as Disciplinas
```http
GET /api/disciplinas/
```

**Resposta (200 OK):**
```json
[
  {
    "id": 1,
    "nome": "Cálculo I",
    "codigo": "MAT101"
  },
  {
    "id": 2,
    "nome": "Programação Orientada a Objetos",
    "codigo": "INF202"
  }
]
```

---

#### **4. Registros de Monitoria (Monitor TEA)**

##### Listar Registros do Monitor TEA
```http
GET /api/registros-monitoria/
```

**Resposta (200 OK):**
```json
[
  {
    "id": 5,
    "data_monitoria": "2025-11-10",
    "horario_inicio": "14:00:00",
    "horario_fim": "16:00:00",
    "horas_trabalhadas": "2.00",
    "codigo_disciplina": "MAT101",
    "descricao_atividade": "Monitoria de exercícios de derivadas",
    "quantidade_alunos": 5,
    "alunos_participantes": [
      {"nome": "Maria Silva", "matricula": "202311000001"},
      {"nome": "João Santos", "matricula": "202311000002"}
    ]
  }
]
```

##### Criar Registro de Monitoria
```http
POST /api/registros-monitoria/
Content-Type: application/json

{
  "candidatura_id": 10,
  "data_monitoria": "2025-11-12",
  "horario_inicio": "14:00",
  "horario_fim": "16:00",
  "descricao_atividade": "Resolução de exercícios práticos",
  "alunos_participantes": [
    {"nome": "Ana Costa", "matricula": "202311000003"},
    {"nome": "Pedro Lima", "matricula": "202311000004"}
  ],
  "observacoes": "Boa participação dos alunos"
}
```

---

#### **5. Aprovação de Candidaturas (Professor/Coordenador/Casa)**

##### Aprovar Candidatura
```http
POST /api/candidaturas/{id}/aprovar/
```

**Resposta (200 OK):**
```json
{
  "message": "Candidatura aprovada com sucesso",
  "monitor_criado": true,
  "tipo_monitor": "Monitor"
}
```

##### Rejeitar Candidatura
```http
POST /api/candidaturas/{id}/rejeitar/
```

**Resposta (200 OK):**
```json
{
  "message": "Candidatura rejeitada"
}
```

---

### 📝 Exemplos de Uso com cURL

#### Listar Vagas
```bash
curl -X GET http://127.0.0.1:8000/api/vagas/
```

#### Criar Candidatura
```bash
curl -X POST http://127.0.0.1:8000/api/candidaturas/ \
  -H "Content-Type: application/json" \
  -d '{
    "vaga_id": 1,
    "cr_disciplina": 8.5,
    "documentos": "Histórico anexado"
  }'
```

#### Aprovar Candidatura
```bash
curl -X POST http://127.0.0.1:8000/api/candidaturas/10/aprovar/
```

---

### 📝 Exemplos com Python (requests)

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Listar todas as vagas
response = requests.get(f"{BASE_URL}/vagas/")
vagas = response.json()
print(vagas)

# Criar candidatura
candidatura_data = {
    "vaga_id": 1,
    "cr_disciplina": 8.5,
    "documentos": "Histórico escolar"
}
response = requests.post(f"{BASE_URL}/candidaturas/", json=candidatura_data)
print(response.json())

# Listar disciplinas
response = requests.get(f"{BASE_URL}/disciplinas/")
disciplinas = response.json()
for disciplina in disciplinas:
    print(f"{disciplina['codigo']} - {disciplina['nome']}")
```

---

### 📝 Exemplos com JavaScript (Fetch API)

```javascript
const BASE_URL = 'http://127.0.0.1:8000/api';

// Listar vagas
fetch(`${BASE_URL}/vagas/`)
  .then(response => response.json())
  .then(data => console.log(data));

// Criar candidatura
fetch(`${BASE_URL}/candidaturas/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    vaga_id: 1,
    cr_disciplina: 8.5,
    documentos: 'Histórico escolar anexado'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Aprovar candidatura
fetch(`${BASE_URL}/candidaturas/10/aprovar/`, {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 📁 Estrutura do Projeto

```
PBE_25.2_8004_III/
├── docs/                          # Documentação MkDocs
│   ├── Iniciacao/                # Documentos de iniciação
│   ├── Elaboracao/               # Diagramas UML
│   │   ├── diagrama_de_classes.md
│   │   ├── casos_de_uso.md
│   │   └── diagrama_de_sequencia.md
│   ├── Construcao/               # Documentos de construção
│   └── Transicao/                # Documentos de transição
├── src/                          # Código-fonte
│   ├── myapp/                    # Aplicação Django principal
│   │   ├── models.py            # Modelos (11 classes)
│   │   ├── views.py             # Views (20+ endpoints)
│   │   ├── api.py               # ViewSets da API REST
│   │   ├── serializers.py       # Serializers DRF
│   │   ├── urls.py              # URLs da aplicação
│   │   ├── api_urls.py          # URLs da API
│   │   ├── admin.py             # Admin do Django
│   │   ├── tests.py             # Testes unitários
│   │   ├── static/              # Arquivos estáticos
│   │   │   ├── css/             # Estilos CSS
│   │   │   ├── js/              # Scripts JavaScript
│   │   │   ├── img/             # Imagens
│   │   │   └── fonts/           # Fontes customizadas
│   │   ├── template/            # Templates HTML
│   │   └── migrations/          # Migrações do banco
│   ├── myproject/               # Configurações do projeto
│   │   ├── settings.py          # Configurações Django
│   │   ├── urls.py              # URLs principais
│   │   └── wsgi.py              # WSGI config
│   ├── manage.py                # Script de gerenciamento
│   └── db.sqlite3               # Banco de dados
├── requirements.txt             # Dependências Python
├── mkdocs.yml                   # Configuração MkDocs
└── README.md                    # Este arquivo
```

---

## 🔐 Regras de Negócio Principais

### Candidatura
- **RN20**: CR geral mínimo: 7.0
- **RN21**: CR na disciplina mínimo: 8.0
- **RN22**: Não permite candidaturas duplicadas (aluno + vaga)
- **RN23**: Status inicial sempre 'Pendente'

### Vaga
- **RN10**: Apenas coordenadores e Casa podem criar vagas
- **RN11**: Prazo de inscrição deve ser futuro
- **RN12**: Status inicial sempre 'Aberta'

### Aprovação
- **RN28**: Aprovação cria automaticamente registro de Monitor ou MonitorTEA
- **RN29**: Uso de get_or_create evita duplicação de monitores
- **RN30**: Alunos NÃO podem aprovar candidaturas

---

## 📚 Documentação Adicional

A documentação completa está disponível em:
- **Diagrama de Classes**: `docs/Elaboracao/diagrama_de_classes.md`
- **Casos de Uso**: `docs/Elaboracao/casos_de_uso.md`
- **Diagramas de Sequência**: `docs/Elaboracao/diagrama_de_sequencia.md`

Para visualizar a documentação renderizada:
```bash
mkdocs serve
```
Acesse: **http://127.0.0.1:8000**

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Minha nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato

**Instituição**: IBMEC  
**Disciplina**: Projeto Back-End (IBM8936)  
**Período**: 2025.2  
**Repositório**: [PBE_25.2_8004_III](https://github.com/Projetos-de-Extensao/PBE_25.2_8004_III)

---

<div align="center">
  <p>Desenvolvido com ❤️ pela equipe do Projeto Back-End Frello 2025.2</p>
  <p>IBMEC © 2025</p>
</div>
 