---
id: diagrama_de_classes
title: Diagrama de Classes
---

## Classes

### Descrição: 
Este documento apresenta o **Diagrama de Classes** da plataforma de monitoria da IBMEC. O diagrama representa as principais entidades do sistema e seus relacionamentos, servindo como base para o desenvolvimento do **back-end** da aplicação.

### **Objetivo**
O diagrama tem como objetivo organizar a estrutura de dados da plataforma, definindo claramente os atributos e relacionamentos das classes principais, de modo que o desenvolvimento seja consistente e alinhado aos requisitos do projeto.


- Aluno
	- Nome
	- Matrícula
	- Email
	- Telefone
	- Cr Geral
	- Cr disciplina
	- Curso
	- Senha

- Professor
	- Nome
	- Matrícula
	- Email
	- Telefone
	- Senha

- Vaga 	
    - Nome
	- Identificador
	- Pré-requisitos
	- Disciplina
	- Status
	- Prazo de inscrição

- Candidatura 
	- Id
	- Aluno
	- Vaga
	- Documentos
	- Status
	- Data da candidatura

- Registro de Monitoria
	- Id
	- Aluno
	- Vaga
	- Horas trabalhadas
	- Data de registro
	- Validação

```plantuml
@startuml 
'-----------------------------------
' Diagram: Plataforma de Monitoria
'-----------------------------------

class Aluno {
	+ nome: string 
	+ matricula: string
	+ email: string
	+ telefone: string
	+ crGeral: float
	+ crDisciplina: float
	+ curso: string
	+ senha: string
}

class Professor {
	+ nome: string 
	+ matricula: string
	+ email: string
	+ telefone: string
	+ senha: string
}

class Vaga {
	+ nome: string 
	+ identificador: int
	+ preRequisitos: string
	+ disciplina: string
	+ status: string
	+ prazoInscricao: date
}

class Candidatura {
	+ id: int
	+ aluno: Aluno
	+ vaga: Vaga
	+ documentos: string
	+ status: string
	+ dataCandidatura: date
	+ validarCR(): bool
}

class RegistroMonitoria {
	+ id: int
	+ aluno: Aluno
	+ vaga: Vaga
	+ horasTrabalhadas: float
	+ dataRegistro: date
	+ validadoPor: Professor
}

Aluno -> Candidatura: realiza
Vaga -> Candidatura: recebe
Professor -> Vaga: cadastra
Candidatura -> RegistroMonitoria: gera

@enduml
```