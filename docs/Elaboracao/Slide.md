---
marp: true
theme: default
paginate: true
title: Plataforma de Monitoria - Frello
---

# Plataforma de Monitoria  
## Especificação de Requisitos

**Projeto de Gestão de Candidaturas e Monitoria**

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

A Plataforma de Monitoria tem como objetivo centralizar e gerenciar vagas de monitoria para alunos da faculdade, permitindo candidaturas rápidas, automação do processo seletivo e histórico das candidaturas.

**Escopo:**
- Gestão de vagas de monitoria
- Cadastro e autenticação de alunos
- Processo seletivo automatizado
- Painel administrativo para professores/admins
- Notificações automáticas e histórico

---

# Requisitos Funcionais

- Cadastro e login via e-mail institucional
- Validação do vínculo com a faculdade
- Visualização de vagas em tempo real
- Upload de documentos obrigatórios
- Restrição: uma vaga por disciplina/semestre
- Acompanhamento automático do status da candidatura
- Histórico de candidaturas
- Notificações automáticas por e-mail
- Cadastro e arquivamento de vagas (admin)
- Visualização, filtragem e avaliação de candidatos (admin)
- Exportação de relatórios (PDF/Excel)

---

# Requisitos Não Funcionais

- **Segurança:** Senhas criptografadas (ex: bcrypt)
- **Performance:** Resposta em até 2 segundos para vagas
- **Disponibilidade:** 99% no horário acadêmico
- **Usabilidade:** Interface responsiva e mobile-friendly
- **Confiabilidade:** Logs de todas as ações administrativas e candidaturas

---

# Regras de Negócio

- Apenas alunos com e-mail institucional podem se cadastrar
- Cada aluno só pode se candidatar a uma vaga por disciplina/semestre
- Apenas professores/admins podem cadastrar vagas
- Vagas encerradas são arquivadas automaticamente
- Alterações no status da candidatura são registradas no histórico

---

# Casos de Uso: Visão Geral

- Criar conta (e-mail institucional)
- Validar vínculo com faculdade
- Aceitar termos de uso
- Completar perfil
- Visualizar vagas disponíveis
- **Validação de candidatura (CR)**
- Candidatar-se à vaga
- Upload de documentos obrigatórios
- Receber notificações por e-mail
- Visualizar status e histórico de candidaturas
- Cadastro e gestão de vagas (admin)
- Gerenciar e filtrar candidatos (admin)
- Exportar relatórios (admin)

---

## Caso de Uso: Validação de candidatura

**Ator:** Sistema  
**Descrição:** Valida automaticamente se o aluno atende aos critérios mínimos de CR para se candidatar a uma vaga.  
**Pré-condição:** Aluno selecionou vaga e iniciou candidatura.  
**Fluxo Principal:**  
1. Sistema consulta o CR geral do aluno  
2. Sistema consulta o CR do aluno na disciplina da vaga  
3. Verifica se CR geral ≥ 7  
4. Verifica se CR da disciplina ≥ 8  
5. Se ambos atendidos, permite prosseguir  
**Fluxo Alternativo:**  
- Se CR geral < 7 ou CR da disciplina < 8: bloqueia candidatura e exibe mensagem  
**Pós-condição:** Candidatura permitida ou bloqueada  
**Regras de Negócio:** CR geral ≥ 7 e CR da disciplina ≥ 8

---

## Caso de Uso: Candidatar-se à vaga

**Ator:** Aluno  
**Descrição:** Permite ao aluno se candidatar a uma vaga.  
**Pré-condição:** Perfil completo, vaga disponível e validação de candidatura aprovada.  
**Fluxo Principal:**  
1. Aluno seleciona vaga  
2. Aluno envia candidatura  
3. Sistema solicita upload de documentos obrigatórios  
4. Sistema envia notificação por e-mail  
5. Sistema atualiza status da candidatura  
**Fluxo Alternativo:**  
- Documentos não enviados: candidatura não é concluída  
**Pós-condição:** Candidatura registrada e notificada  
**Regras de Negócio:** Documentação obrigatória

---

# Finalização

- Plataforma centraliza e automatiza o processo de monitoria
- Garante critérios justos e históricos completos
- Atende requisitos de segurança, usabilidade e confiabilidade
- Facilita a gestão para alunos, professores e administradores

**Dúvidas? Obrigado!**