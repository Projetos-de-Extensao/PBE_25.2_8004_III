# Especificação de Requisitos – Plataforma de Monitoria

---

## 1. Introdução
Este documento descreve os requisitos funcionais e não funcionais da plataforma de monitoria da faculdade, cujo objetivo é centralizar e gerenciar vagas de monitoria para os alunos. A plataforma permitirá candidaturas rápidas e simplificadas, automatizará parte do processo seletivo e manterá histórico das candidaturas, garantindo uma experiência simples e intuitiva.

**Escopo do Sistema:**
- Gestão de vagas de monitoria.
- Cadastro e autenticação de alunos.
- Processo seletivo automatizado.
- Painel administrativo para professores e administradores.
- Notificações automáticas e histórico de candidaturas.

**Definições importantes:**
- **Aluno:** Estudante que pode se candidatar às vagas de monitoria.
- **Professor:** Usuário que cadastra e gerencia vagas.
- **Vaga:** Registro de oportunidade de monitoria.
- **Candidatura:** Inscrição do aluno em uma vaga.
- **RegistroMonitoria:** Controle de horas de monitoria.

---

## 2. Visão Geral do Sistema
A plataforma permite que alunos visualizem e se candidatem às vagas de monitoria e que professores ou administradores gerenciem essas vagas e o processo seletivo.  

**Principais Funcionalidades:**
- Cadastro de alunos e validação de vínculo institucional.
- Publicação e gerenciamento de vagas de monitoria.
- Inscrição de alunos com upload de documentos.
- Avaliação, aprovação e comunicação de candidatos.
- Histórico de candidaturas e relatórios administrativos.
- Notificações automáticas por e-mail.
- Interface simples e intuitiva para todos os usuários.

**Restrições:**
- Apenas alunos com e-mail institucional podem se cadastrar.
- Cada aluno só pode se candidatar a uma vaga por disciplina a cada semestre.
- Apenas professores ou administradores podem cadastrar vagas.

---

## 3. Requisitos Funcionais

### Painel do Aluno
- **RF01 [BS01]:** Cadastro e login via e-mail institucional.  
- **RF02 [BS02]:** Validação do vínculo com a faculdade.  
- **RF03 [BS03]:** Visualização de todas as vagas em tempo real.  
- **RF04 [BS05]:** Upload de documentos obrigatórios durante candidatura.  
- **RF05 [BS09]:** Restrição de candidatura: Admin determinan número de vagas por disciplina por semestre.  
- **RF06 [BS08]:** Acompanhamento automático do status da candidatura.  
- **RF07 [BS12]:** Acesso a histórico de candidaturas.  
- **RF08 [BS14]:** Notificações automáticas por e-mail sobre alterações de status.

### Painel Administrativo
- **RF09 [BS04]:** Cadastro de novas vagas com informações detalhadas.  
- **RF10 [BS11]:** Arquivamento automático de vagas encerradas.  
- **RF11 [BS07]:** Visualização e filtragem de candidatos por vaga.  
- **RF12:** Avaliação de candidatos e acesso a documentos enviados.  
- **RF13 [BS13]:** Alteração de status da candidatura no processo seletivo.  
- **RF14 [BS10]:** Exportação de relatórios em PDF ou Excel.  

### Funcionalidades Gerais do Sistema
- **RF15 [BS06]:** Envio automático de e-mails para candidatos.  
- **RF16 [BS15]:** Interface simples e intuitiva.  
- **RF17:** Armazenamento de histórico completo de candidaturas.

---

## 4. Requisitos Não Funcionais
- **RNF01 – Segurança:** Todas as senhas devem ser criptografadas com hash seguro (ex.: bcrypt).  
- **RNF02 – Performance:** O sistema deve responder em menos de 2 segundos ao carregar as vagas disponíveis.  
- **RNF03 – Disponibilidade:** Disponibilidade mínima de 99% durante o horário acadêmico.  
- **RNF04 – Usabilidade:** Interface deve ser responsiva e compatível com dispositivos móveis.  
- **RNF05 – Confiabilidade:** Sistema deve registrar logs de todas as ações administrativas e candidaturas.

---

## 5. Regras de Negócio
- **RN01:** Apenas alunos com e-mail institucional válido podem se cadastrar.  
- **RN02:** Cada aluno pode se candidatar a uma ou mais vagas por disciplina por semestre.  
- **RN03:** Apenas professores ou administradores podem cadastrar vagas.  
- **RN04:** Vagas encerradas são automaticamente arquivadas pelo sistema.  
- **RN05:** Alterações no status da candidatura devem ser registradas no histórico do aluno.  

---

## 6. Interfaces Externas
- Integração com servidor de e-mail para envio de notificações automáticas.  
- Banco de dados relacional para armazenamento de usuários, vagas e candidaturas.  

---

## 7. Restrições
- Cadastro limitado a alunos da instituição com e-mail institucional.  
- Cada disciplina permite uma quantidade pré-definida de monitores por semestre.  
- Processos seletivos devem seguir o calendário acadêmico definido pelo departamento.

---

## 8. Critérios de Aceitação
- Alunos conseguem criar conta e se candidatar a vagas corretamente.  
- Professores podem cadastrar e gerenciar vagas.  
- Status da candidatura é atualizado corretamente no painel do aluno.  
- Sistema envia notificações automáticas em todos os eventos relevantes.  
- Relatórios podem ser exportados em PDF ou Excel sem perda de dados.  

---

## 9. Glossário
- **Aluno:** Estudante apto a se candidatar às vagas de monitoria.  
- **Professor:** Usuário responsável por cadastrar vagas e gerenciar candidaturas.  
- **Vaga:** Registro de oportunidade de monitoria.  
- **Candidatura:** Inscrição do aluno em uma vaga.  
- **RegistroMonitoria:** Controle de horas de monitoria de cada aluno.

---

## 10. Referências
- Requisitos elicitados BS01 a BS15 (conforme levantamento interno).  
- Normas de segurança de dados acadêmicos.  
- Material de boas práticas de UX/UI para plataformas educacionais.

## **Autor(es)**
| Data | Versão | Descrição | Autor(es) |
|-------|--------|-----------|------------|
| 18/09/2025 | 1.0 | Criação do documento | Sarah Ferrari.