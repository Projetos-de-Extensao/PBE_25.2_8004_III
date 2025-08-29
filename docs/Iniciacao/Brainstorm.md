---
id: brainstorm
title: Brainstorm
---

## **Introdução**
<p align="justify">
O brainstorm é uma técnica de elicitação de requisitos que consiste em reunir a equipe e discutir sobre diversos tópicos gerais do projeto apresentados no documento problema de negócio. No brainstorm o diálogo é incentivado e críticas são evitadas para permitir que todos colaborem com suas próprias ideias.
</p>

---

## **Metodologia**
<p align = "justify">
A equipe se reuniu para debater ideias gerais sobre o projeto via..., começou .... e terminou..., onde o XXXX XXXX foi o moderador, direcionando a equipe com questões pré-elaboradas, e transcrevendo as respostas para o documento.
</p>
---

## **Brainstorm**

### **Versão 1.0**

---

### **1. Qual o objetivo principal da aplicação?**
<p align="justify">

- A plataforma deve centralizar todas as vagas de monitoria da faculdade para facilitar o acesso dos alunos.  
   
- O sistema deve permitir candidaturas rápidas e simplificadas.

- A aplicação deve automatizar parte do processo de aprovação dos candidatos.
    
- O foco é ser simples e intuitivo, garantindo que todos entendam como usar.
     
- A plataforma também deve armazenar um histórico das candidaturas para futuras consultas.   
</p>

---

### **2. Como será o processo para cadastrar um novo aluno (candidato)?**
<p align="justify"> 
  
- O aluno acessa a plataforma, cria um cadastro com e-mail institucional e senha.
  
- O sistema deve validar o vínculo com a instituição (ex: e-mail verificado
  
- Após o login, o aluno poderá completar o perfil com informações pessoais e acadêmicas.
  
- O aluno deverá aceitar os termos de uso antes de finalizar o cadastro.
  
- O cadastro deve ser simples para não desestimular novos usuários.
</p>

---

### **3. Como será a forma de adicionar vagas de monitoria?**
<p align="justify">
  
- Apenas professores ou administradores poderão cadastrar novas vagas.
  
- As vagas devem conter informações como disciplina, pré-requisitos e prazo de inscrição.

- O sistema deve permitir upload de documentos relacionados à vaga (ex: plano de atividades).
  
- É importante que as vagas fiquem visíveis em tempo real para os alunos.
  
- Vagas encerradas devem ser automaticamente arquivadas.
</p>

---

### **4. Como será a candidatura às vagas?**
<p align="justify"> 

- O aluno logado poderá clicar em “Candidatar-se” diretamente na vaga.
  
- Será necessário anexar documentos obrigatórios, como histórico acadêmico.
  
- O sistema deve confirmar a inscrição e enviar uma notificação por e-mail.
   
- Cada aluno só pode se candidatar a uma vaga por disciplina por semestre.
  
- O status da candidatura deve ser atualizado automaticamente no painel do aluno.
</p>

---

### **5. Quais funcionalidades o painel administrativo deve ter?**
<p align="justify">  
  
- Visualizar todos os candidatos inscritos em cada vaga.
  
- Filtrar candidatos por critérios como média, curso ou histórico de monitoria.
  
- Alterar status do processo seletivo: "Em análise", "Aprovado", "Reprovado".
  
- Exportar listas de candidatos em PDF ou Excel.
  
- Histórico de processos seletivos para auditoria.
</p>

---

### **6. Quais informações seriam interessantes para os alunos?**
<p align="justify"> 
  
- Histórico de vagas que já se candidatou.
  
- Status atualizado da candidatura. 
   
- Prazo de cada processo seletivo.
  
- Pré-requisitos e informações detalhadas da vaga.
  
- Notificações sobre alterações no processo.
</p>

---

## **Requisitos Elicitados**

| ID   | Descrição |
|-------|-----------|
| BS01  | O sistema deve permitir que alunos criem contas com autenticação pelo e-mail institucional. |
| BS02  | O sistema deve validar o vínculo do usuário com a faculdade. |
| BS03  | Alunos devem conseguir visualizar todas as vagas disponíveis em tempo real. |
| BS04  | Professores e administradores devem cadastrar novas vagas com informações detalhadas. |
| BS05  | O sistema deve permitir upload de documentos obrigatórios durante a candidatura. |
| BS06  | O sistema deve enviar notificações automáticas por e-mail aos candidatos. |
| BS07  | O painel administrativo deve permitir a visualização, filtragem e gerenciamento de candidatos. |
| BS08  | O sistema deve atualizar automaticamente o status da candidatura no painel do aluno. |
| BS09  | Apenas uma candidatura por disciplina será permitida por semestre. |
| BS10  | O painel administrativo deve permitir exportar listas em PDF ou Excel. |
| BS11  | Vagas encerradas devem ser arquivadas automaticamente. |
| BS12  | O sistema deve armazenar histórico de candidaturas para consulta futura. |
| BS13  | O painel administrativo deve permitir alterações de status no processo seletivo. |
| BS14  | Alunos devem receber notificações sobre mudanças no status da candidatura. |
| BS15  | O sistema deve garantir interface simples e intuitiva para todos os perfis de usuários. |

---

## **Conclusão**
<p align="justify">
Através da aplicação da técnica de brainstorm, foi possível elicitar os primeiros requisitos da plataforma de monitoria. Esses requisitos servirão como base para a modelagem do sistema e para o planejamento da arquitetura do back-end, que será o foco principal do desenvolvimento.
</p>

---

## **Referências Bibliográficas**
> BARBOSA, S. D. J; DA SILVA, B. S. Interação humano-computador. Elsevier, 2010.

---

## **Autor(es)**
| Data | Versão | Descrição | Autor(es) |
|-------|--------|-----------|------------|
| 28/08/2025 | 1.0 | Criação do documento | Sarah Ferrari, João Mariano, João Victor, João Donda e Caique Rechuan.
