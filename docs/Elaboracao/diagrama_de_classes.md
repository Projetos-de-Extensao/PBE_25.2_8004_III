---
id: diagrama_de_classes
title: Diagrama de Classes
---

## Classes

### Descrição:

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
	- Documentos
	- Pré-requisitos
	- Disciplina
	- Status
	- Prazo de inscrição

@startuml 

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
	+ documentos: string
	+ preRequisitos: string
	+ disciplina: string
	+ status: string
	+ prazoInscricao: date
}

Aluno -> Vaga: se candidata
Professor -> Vaga: cadastra

@enduml