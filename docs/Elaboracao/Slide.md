---
marp: true
theme: default
paginate: true
title: Plataforma de Monitoria - Frello
---

# Plataforma de Monitoria  
## Especificação de Requisitos

Projeto de Gestão de Candidaturas e Monitoria

---

## Sumário

1. Introdução  
2. Requisitos Funcionais  
3. Requisitos Não Funcionais  
4. Regras de Negócio  
5. Casos de Uso: Visão Geral  
6. Exemplos de Casos de Uso  
7. Finalização

---

# Introdução

Centraliza e gerencia vagas de monitoria para alunos, com candidaturas rápidas, automação do processo seletivo e histórico.

**Escopo:**
- Gestão de vagas
- Cadastro/autenticação de alunos
- Processo seletivo automatizado
- Painel para professores/admins
- Notificações e histórico

---

# Requisitos Funcionais

- Cadastro/login institucional
- Validação de vínculo
- Visualização de vagas
- Upload de documentos
- 1 vaga por disciplina/semestre
- Acompanhamento de status
- Histórico de candidaturas
- Notificações por e-mail
- Cadastro/arquivamento de vagas (admin)
- Gestão e filtro de candidatos (admin)
- Exportação de relatórios

---

# Requisitos Não Funcionais

- **Segurança:** Senhas criptografadas
- **Performance:** Resposta rápida
- **Disponibilidade:** 99% no horário acadêmico
- **Usabilidade:** Interface responsiva
- **Confiabilidade:** Logs de ações

---

# Regras de Negócio

- Apenas e-mail institucional no cadastro
- 1 vaga por disciplina/semestre por aluno
- Só professores/admins cadastram vagas
- Vagas encerradas são arquivadas
- Histórico de alterações de status

---

# Casos de Uso: Visão Geral

- Criar conta
- Validar vínculo
- Aceitar termos
- Completar perfil
- Visualizar vagas
- Validação de candidatura (CR)
- Candidatar-se à vaga
- Upload de documentos
- Notificações por e-mail
- Visualizar status/histórico
- Cadastro/gestão de vagas (admin)
- Gerenciar/filtrar candidatos (admin)
- Exportar relatórios (admin)

---

# Caso de Uso: Validação de candidatura

**Ator:** Sistema  
Valida se o aluno atende aos critérios de CR para candidatura.

- Pré: Vaga selecionada, candidatura iniciada
- Passos:
  1. Consulta CR geral e da disciplina
  2. Verifica CR geral ≥ 7 e CR disciplina ≥ 8
  3. Permite ou bloqueia candidatura
- Pós: Candidatura permitida ou bloqueada  
- Regra: CR geral ≥ 7 e CR disciplina ≥ 8

---

# Caso de Uso: Candidatar-se à vaga

**Ator:** Aluno  
Permite candidatura a uma vaga.

- Pré: Perfil completo, vaga disponível, validação aprovada
- Passos:
  1. Seleciona vaga
  2. Envia candidatura
  3. Faz upload de documentos
  4. Recebe notificação
  5. Status atualizado
- Pós: Candidatura registrada/notificada  
- Regra: Documentação obrigatória

---

# Finalização

- Plataforma centraliza e automatiza monitoria
- Critérios justos e históricos completos
- Segurança, usabilidade e confiabilidade
- Facilita gestão para todos os usuários

**Dúvidas? Obrigado!**