---
id: diagrama_de_sequencia
title: Diagramas de Sequência
---

# Diagramas de Sequência - Sistema de Monitoria IBMEC

## Descrição
Este documento apresenta os **Diagramas de Sequência** dos principais fluxos implementados no Sistema de Monitoria IBMEC. Cada diagrama representa fielmente as interações entre objetos, métodos e camadas do sistema conforme desenvolvido.

---

## DS01 - Cadastro de Aluno

Representa o fluxo completo desde o acesso à página de cadastro até a criação do registro e autenticação automática.

```plantuml
@startuml
actor Aluno
participant "Browser" as Browser
participant "views.cadastro_aluno" as View
participant "Aluno Model" as AlunoModel
participant "bcrypt" as Bcrypt
participant "Database" as DB
participant "Session" as Session

Aluno -> Browser: Acessa /cadastro_aluno/
Browser -> View: GET request

alt Método GET
    View -> Browser: Renderiza formulário de cadastro
    Browser -> Aluno: Exibe página com formulário
end

Aluno -> Browser: Preenche dados (nome, email, matrícula, CR, senha)
Browser -> View: POST request com dados

alt Método POST
    View -> AlunoModel: Busca por email
    AlunoModel -> DB: SELECT WHERE email = ?
    DB -> AlunoModel: Resultado
    
    alt Email já existe
        AlunoModel -> View: Aluno encontrado
        View -> Browser: Renderiza com mensagem "Email já cadastrado"
        Browser -> Aluno: Exibe erro
    else Email não existe
        View -> AlunoModel: Busca por matrícula
        AlunoModel -> DB: SELECT WHERE matricula = ?
        DB -> AlunoModel: Resultado
        
        alt Matrícula já existe
            AlunoModel -> View: Aluno encontrado
            View -> Browser: Renderiza com mensagem "Matrícula já cadastrada"
            Browser -> Aluno: Exibe erro
        else Matrícula disponível
            View -> Bcrypt: hashpw(senha, gensalt())
            Bcrypt -> View: senha_hash
            
            View -> AlunoModel: Cria instância Aluno
            Note right: nome, email, matricula, cr_geral, curso, senha_hash
            AlunoModel -> DB: INSERT INTO myapp_aluno
            DB -> AlunoModel: Confirmação (ID gerado)
            
            View -> Session: Cria sessão
            Note right: user_id, user_type='aluno', user_name
            Session -> View: Confirmação
            
            View -> Browser: Redirect para /painel_aluno/
            Browser -> Aluno: Redireciona para painel
        end
    end
end

@enduml
```

**Objetos Envolvidos:**
- `Aluno` (usuário)
- `views.cadastro_aluno` (controlador)
- `Aluno Model` (modelo Django)
- `bcrypt` (biblioteca de criptografia)
- `Database` (SQLite/PostgreSQL)
- `Session` (Django session framework)

**Mensagens Principais:**
1. GET: Renderiza formulário
2. POST: Valida email → Valida matrícula → Criptografa senha → Cria registro → Autentica → Redireciona

---

## DS02 - Login de Usuário

Representa autenticação multi-perfil com identificação automática do tipo de usuário.

```plantuml
@startuml
actor Usuario
participant "Browser" as Browser
participant "views.login" as View
participant "Aluno Model" as AlunoModel
participant "Professor Model" as ProfessorModel
participant "Coordenador Model" as CoordenadorModel
participant "Casa Model" as CasaModel
participant "Monitor Model" as MonitorModel
participant "bcrypt" as Bcrypt
participant "Session" as Session
participant "Database" as DB

Usuario -> Browser: Acessa /login/
Browser -> View: GET request
View -> Browser: Renderiza formulário de login
Browser -> Usuario: Exibe página

Usuario -> Browser: Informa email e senha
Browser -> View: POST request

View -> AlunoModel: filter(email=email).first()
AlunoModel -> DB: SELECT * FROM myapp_aluno WHERE email = ?
DB -> AlunoModel: Resultado

alt Aluno encontrado
    AlunoModel -> View: Retorna instância Aluno
    View -> Bcrypt: checkpw(senha, aluno.senha_hash)
    Bcrypt -> View: True/False
    
    alt Senha correta
        View -> MonitorModel: filter(matricula=aluno.matricula).exists()
        MonitorModel -> DB: SELECT COUNT(*) FROM myapp_monitor WHERE matricula = ?
        DB -> MonitorModel: 0 ou 1
        
        alt É monitor
            View -> Session: Define user_type='monitor'
        else Não é monitor
            View -> Session: Define user_type='aluno'
        end
        
        View -> Session: Define user_id, user_name
        View -> Browser: Redirect conforme user_type
        Browser -> Usuario: Redireciona para painel
    else Senha incorreta
        View -> Browser: Renderiza com erro genérico
        Browser -> Usuario: "Email ou senha inválidos"
    end
else Aluno não encontrado
    View -> ProfessorModel: filter(email=email).first()
    ProfessorModel -> DB: SELECT * FROM myapp_professor WHERE email = ?
    DB -> ProfessorModel: Resultado
    
    alt Professor encontrado
        View -> CoordenadorModel: filter(cpf=professor.cpf).exists()
        CoordenadorModel -> DB: SELECT COUNT(*) FROM myapp_coordenador WHERE cpf = ?
        DB -> CoordenadorModel: 0 ou 1
        
        alt É coordenador
            View -> Session: Define user_type='coordenador'
            View -> Browser: Redirect para /painel_coordenador/
        else É professor
            View -> Session: Define user_type='professor'
            View -> Browser: Redirect para /painel_professor/
        end
    else Professor não encontrado
        View -> CasaModel: filter(email=email).first()
        CasaModel -> DB: SELECT * FROM myapp_casa WHERE email = ?
        
        alt Casa encontrado
            View -> Session: Define user_type='casa'
            View -> Browser: Redirect para /dashboard/
        else Nenhum usuário encontrado
            View -> Browser: Renderiza com erro genérico
            Browser -> Usuario: "Email ou senha inválidos"
        end
    end
end

@enduml
```

**Fluxo de Decisão:**
1. Busca em Aluno → Se encontrado, verifica se é Monitor
2. Se não encontrado, busca em Professor → Verifica se é Coordenador
3. Se não encontrado, busca em Casa
4. Se nada encontrado, retorna erro genérico (segurança)

---

## DS03 - Candidatura a Vaga

Representa o fluxo completo de candidatura com validação automática de CR.

```plantuml
@startuml
actor Aluno
participant "Browser" as Browser
participant "views.candidatar_vaga" as View
participant "VagaMonitoria Model" as VagaModel
participant "Candidatura Model" as CandidaturaModel
participant "Aluno Model" as AlunoModel
participant "Session" as Session
participant "Database" as DB

Aluno -> Browser: Clica em "Candidatar-se" na vaga
Browser -> View: GET /candidatar_vaga/<vaga_id>/

View -> Session: Obtém user_id e user_type
Session -> View: user_id, user_type

alt user_type != 'aluno'
    View -> Browser: Redirect com mensagem "Acesso negado"
    Browser -> Aluno: Exibe erro
else user_type == 'aluno'
    View -> VagaModel: get(id=vaga_id)
    VagaModel -> DB: SELECT * FROM myapp_vagamonitoria WHERE id = ?
    DB -> VagaModel: Resultado vaga
    VagaModel -> View: Retorna vaga
    
    alt Vaga não encontrada
        View -> Browser: Retorna 404
    else Vaga encontrada
        View -> AlunoModel: get(matricula=user_id)
        AlunoModel -> DB: SELECT * FROM myapp_aluno WHERE matricula = ?
        DB -> AlunoModel: Dados do aluno
        AlunoModel -> View: Retorna aluno
        
        View -> Browser: Renderiza formulário de candidatura
        Browser -> Aluno: Exibe formulário (CR disciplina, documentos)
        
        Aluno -> Browser: Preenche CR disciplina e documentos
        Browser -> View: POST request
        
        View -> View: Extrai cr_disciplina e documentos
        
        ' Validação automática
        View -> CandidaturaModel: Cria instância temporária
        Note right: aluno=aluno, vaga=vaga, cr_disciplina, documentos
        
        View -> CandidaturaModel: validarCR()
        CandidaturaModel -> AlunoModel: Obtém cr_geral
        AlunoModel -> CandidaturaModel: cr_geral
        
        CandidaturaModel -> CandidaturaModel: Verifica cr_geral >= 7.0
        CandidaturaModel -> CandidaturaModel: Verifica cr_disciplina >= 8.0
        
        alt CR geral < 7.0
            CandidaturaModel -> View: Retorna False
            View -> Browser: Renderiza com erro "CR geral insuficiente"
            Browser -> Aluno: Exibe mensagem de erro
        else CR disciplina < 8.0
            CandidaturaModel -> View: Retorna False
            View -> Browser: Renderiza com erro "CR disciplina insuficiente"
            Browser -> Aluno: Exibe mensagem de erro
        else Ambos CRs válidos
            CandidaturaModel -> View: Retorna True
            
            View -> CandidaturaModel: save()
            CandidaturaModel -> DB: INSERT INTO myapp_candidatura
            Note right: status='Pendente', data_candidatura=hoje
            DB -> CandidaturaModel: Confirmação (ID gerado)
            
            View -> Browser: Redirect para /painel_aluno/ com mensagem sucesso
            Browser -> Aluno: "Candidatura enviada com sucesso!"
        end
    end
end

@enduml
```

**Validações Implementadas:**
- Permissão: Apenas aluno pode candidatar-se
- CR geral ≥ 7.0
- CR disciplina ≥ 8.0
- Vaga deve existir e estar aberta

---

## DS04 - Aprovar Candidatura

Representa aprovação de candidatura por professor/coordenador/casa com criação automática de Monitor.

```plantuml
@startuml
actor "Professor/Coordenador/Casa" as Aprovador
participant "Browser" as Browser
participant "views.aprovar_candidatura" as View
participant "Candidatura Model" as CandidaturaModel
participant "VagaMonitoria Model" as VagaModel
participant "Monitor Model" as MonitorModel
participant "MonitorTEA Model" as MonitorTEAModel
participant "Aluno Model" as AlunoModel
participant "Session" as Session
participant "Database" as DB

Aprovador -> Browser: Clica em "Aprovar" na candidatura
Browser -> View: GET /aprovar_candidatura/<candidatura_id>/

View -> Session: Obtém user_type
Session -> View: user_type

alt user_type not in ['professor', 'coordenador', 'casa']
    View -> Browser: Redirect com "Acesso negado"
else Permissão válida
    View -> CandidaturaModel: get(id=candidatura_id)
    CandidaturaModel -> DB: SELECT * FROM myapp_candidatura WHERE id = ?
    DB -> CandidaturaModel: Dados candidatura
    CandidaturaModel -> View: Retorna candidatura
    
    alt Candidatura não encontrada
        View -> Browser: Retorna 404
    else Candidatura encontrada
        alt Status != 'Pendente'
            View -> Browser: Redirect com "Candidatura já processada"
        else Status == 'Pendente'
            View -> CandidaturaModel: Atualiza status='Aprovada'
            CandidaturaModel -> DB: UPDATE myapp_candidatura SET status='Aprovada' WHERE id = ?
            DB -> CandidaturaModel: Confirmação
            
            View -> VagaModel: Obtém vaga via candidatura.vaga
            VagaModel -> View: Retorna vaga
            
            View -> AlunoModel: Obtém aluno via candidatura.aluno
            AlunoModel -> View: Retorna aluno
            
            alt vaga.tipo_monitoria == 'Monitor'
                View -> MonitorModel: get_or_create(matricula=aluno.matricula)
                MonitorModel -> DB: INSERT OR IGNORE INTO myapp_monitor
                DB -> MonitorModel: Monitor criado/obtido
                MonitorModel -> View: (monitor, created)
            else vaga.tipo_monitoria == 'MonitorTEA'
                View -> MonitorTEAModel: get_or_create(matricula=aluno.matricula)
                MonitorTEAModel -> DB: INSERT OR IGNORE INTO myapp_monitor_tea
                DB -> MonitorTEAModel: MonitorTEA criado/obtido
                MonitorTEAModel -> View: (monitor_tea, created)
            end
            
            View -> Browser: Redirect com "Candidatura aprovada com sucesso"
            Browser -> Aprovador: Exibe confirmação
        end
    end
end

@enduml
```

**Lógica Implementada:**
- Verifica permissões (professor/coordenador/casa)
- Atualiza status da candidatura
- Cria Monitor ou MonitorTEA conforme tipo da vaga
- Usa `get_or_create` para evitar duplicação

---

## DS05 - Cadastrar Nova Vaga

Representa criação de vaga por coordenador ou Casa.

```plantuml
@startuml
actor "Coordenador/Casa" as Criador
participant "Browser" as Browser
participant "views.cadastro_vaga" as View
participant "VagaMonitoria Model" as VagaModel
participant "Disciplina Model" as DisciplinaModel
participant "Coordenador Model" as CoordenadorModel
participant "Session" as Session
participant "Database" as DB

Criador -> Browser: Acessa /cadastro_vaga/
Browser -> View: GET request

View -> Session: Obtém user_type e user_id
Session -> View: user_type, user_id

alt user_type not in ['coordenador', 'casa']
    View -> Browser: Redirect com "Acesso negado"
else Permissão válida
    View -> DisciplinaModel: all()
    DisciplinaModel -> DB: SELECT * FROM myapp_disciplina
    DB -> DisciplinaModel: Lista de disciplinas
    DisciplinaModel -> View: Retorna queryset
    
    View -> Browser: Renderiza formulário com select de disciplinas
    Browser -> Criador: Exibe formulário
    
    Criador -> Browser: Preenche dados da vaga
    Note right: disciplina, titulo, pre_requisitos,\ntipo_monitoria, prazo_inscricao
    Browser -> View: POST request
    
    View -> View: Extrai dados do formulário
    
    View -> DisciplinaModel: get(id=disciplina_id)
    DisciplinaModel -> DB: SELECT * FROM myapp_disciplina WHERE id = ?
    DB -> DisciplinaModel: Disciplina
    
    View -> CoordenadorModel: get(cpf=user_id)
    CoordenadorModel -> DB: SELECT * FROM myapp_coordenador WHERE cpf = ?
    DB -> CoordenadorModel: Coordenador
    
    View -> VagaModel: Cria instância VagaMonitoria
    Note right: disciplina=disciplina, coordenador=coordenador,\ntitulo, pre_requisitos, tipo_monitoria,\nprazo_inscricao, status='Aberta'
    
    VagaModel -> DB: INSERT INTO myapp_vagamonitoria
    DB -> VagaModel: Confirmação (ID gerado)
    
    View -> Browser: Redirect para /dashboard/ com mensagem sucesso
    Browser -> Criador: "Vaga cadastrada com sucesso!"
end

@enduml
```

**Validações:**
- Apenas coordenadores e Casa podem criar
- Disciplina deve existir
- Prazo deve ser futuro (validação HTML5)
- Status inicial sempre 'Aberta'

---

## Matriz de Mensagens e Métodos

| Diagrama | Objeto Origem | Mensagem | Objeto Destino | Tipo Retorno |
|----------|---------------|----------|----------------|--------------|
| DS01 | View | `filter(email=email).first()` | Aluno Model | Aluno ou None |
| DS01 | View | `hashpw(senha, gensalt())` | bcrypt | bytes |
| DS01 | Aluno Model | `save()` | Database | void |
| DS02 | View | `checkpw(senha, hash)` | bcrypt | bool |
| DS02 | View | `exists()` | Monitor Model | bool |
| DS03 | Candidatura | `validarCR()` | self | bool |
| DS03 | Candidatura | `save()` | Database | void |
| DS04 | View | `get_or_create(matricula=x)` | Monitor Model | (Monitor, bool) |
| DS05 | View | `all()` | Disciplina Model | QuerySet |
| DS05 | VagaMonitoria | `save()` | Database | void |

---

## Padrões de Sequência Identificados

### 1. Padrão de Autenticação
```
GET → Renderiza formulário → POST → Valida credenciais → Cria sessão → Redireciona
```

### 2. Padrão de CRUD
```
GET → Renderiza formulário → POST → Valida dados → Salva no banco → Redireciona com mensagem
```

### 3. Padrão de Validação de Permissão
```
Request → Obtém user_type da sessão → Verifica permissão → Permite/Nega acesso
```

### 4. Padrão de Criação Automática
```
Aprovação → Verifica tipo monitoria → get_or_create() → Retorna (objeto, created)
```

---

## Observações Técnicas

### Otimizações de Query
- **select_related()**: Usado em dashboard para reduzir queries N+1
- **filter().count()**: Mais eficiente que len(filter())
- **get_or_create()**: Evita duplicação e reduz lógica condicional

### Segurança Implementada
- Hash bcrypt para senhas
- Validação de permissões em todas as views protegidas
- Mensagens genéricas em falhas de login
- Session-based authentication

### Transações
- Django ORM garante atomicidade em operações de save()
- Aprovação de candidatura + criação de monitor é atômica

---

**Última Atualização**: Novembro 2025  
**Versão**: 2.0 - Reflete implementação real do sistema
