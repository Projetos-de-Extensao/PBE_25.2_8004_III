from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import date


# Classe abstrata que serve como base para todos os tipos de usuários do sistema
# Não cria tabela no banco, apenas fornece estrutura comum
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=15)
    senha_hash = models.CharField(max_length=128)

    class Meta:
        abstract = True  # Define que esta classe não gera tabela no banco

    def login(self):
        raise NotImplementedError("Método login() deve ser implementado")

    def logout(self):
        raise NotImplementedError("Método logout() deve ser implementado")

    def alterarSenha(self, nova_senha):
        self.senha_hash = make_password(nova_senha)
        self.save()
        return True


# Estudante da instituição
class Aluno(Usuario):
    matricula = models.CharField(max_length=12, unique=True, primary_key=True)
    cr_geral = models.FloatField()
    cr_disciplina = models.FloatField()
    curso = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.matricula} - {self.nome}"

    def buscarVaga(self, disciplina):
        return VagaMonitoria.objects.filter(disciplina=disciplina, status='Aberta')

    def realizarCandidatura(self, vagaMonitoria):
        return Candidatura.objects.create(
            aluno=self,
            vaga=vagaMonitoria,
            status='Pendente'
        )


# Aluno aprovado para dar monitoria
class Monitor(Aluno):
    class Meta:
        verbose_name = 'Monitor'
        verbose_name_plural = 'Monitores'

    def gerenciarDisponibilidade(self, horario):
        # Lista de horários padrão de segunda a sexta, das 12h às 13h
        horarios = [
            {"dia": "Segunda", "inicio": "12:00", "fim": "13:00"},
            {"dia": "Terça", "inicio": "12:00", "fim": "13:00"},
            {"dia": "Quarta", "inicio": "12:00", "fim": "13:00"},
            {"dia": "Quinta", "inicio": "12:00", "fim": "13:00"},
            {"dia": "Sexta", "inicio": "12:00", "fim": "13:00"}
        ]

        # Lista que armazenará os horários escolhidos
        horario_escolhido = []

        # Adiciona todos os horários na lista de escolhidos
        for horario in horarios:
            horario_escolhido.append(horario)
        
        return horario_escolhido

    # Permite que o monitor TEA registre as horas trabalhadas
    def submeterRelatorioHoras(self, registro):
        # Verifica se o registro tem o método 'submeter' antes de chamar
        if hasattr(registro, 'submeter'):
            return registro.submeter()
        raise ValueError("Registro inválido")

    # Como o monitor TEA aparece quando convertido para texto
    def __str__(self):
        return f"MonitorTEA {self.matricula} - Salário: R$ {self.salario}"


# Professor da instituição
class Professor(Usuario):
    matricula = models.CharField(max_length=12, unique=True, primary_key=True)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return f"{self.matricula} - {self.nome}"


# Professor com responsabilidades administrativas (gerencia programa de monitoria)
class Coordenador(Professor):
    class Meta:
        verbose_name = 'Coordenador'
        verbose_name_plural = 'Coordenadores'

    def cadastrarVaga(self, vaga):
        vaga.save()
        return vaga

    def aprovarCandidatura(self, candidatura):
        candidatura.status = 'Aprovada'
        candidatura.save()
        return candidatura
    
    def rejeitarCandidatura(self, candidatura):
        candidatura.status = 'Rejeitada'
        candidatura.save()
        return candidatura

    def __str__(self):
        return f"Coordenador {self.matricula} - {self.nome}"


# Disciplina/matéria oferecida pela instituição
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


# Oportunidade de monitoria em uma disciplina
class VagaMonitoria(models.Model):
    titulo = models.CharField(max_length=100)
    pre_requisitos = models.TextField()
    disciplina = models.ForeignKey(
        'Disciplina',
        on_delete=models.CASCADE,
        related_name='vagas'
    )
    coordenador = models.ForeignKey(
        'Coordenador',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='vagas_cadastradas'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Aberta', 'Aberta'),
            ('Fechada', 'Fechada'),
            ('Em Análise', 'Em Análise')
        ],
        default='Aberta'
    )
    prazo_inscricao = models.DateField()

    def __str__(self):
        return f"{self.titulo} - {self.disciplina.nome}"

    def verDetalhes(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'pre_requisitos': self.pre_requisitos,
            'disciplina': str(self.disciplina),
            'status': self.status,
            'prazo_inscricao': self.prazo_inscricao.isoformat() if self.prazo_inscricao else None,
        }

    def visualizarCandidaturas(self):
        return self.candidaturas_recebidas.all()


# Candidatura de um aluno a uma vaga de monitoria
class Candidatura(models.Model):
    documentos = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pendente', 'Pendente'),
            ('Aprovada', 'Aprovada'),
            ('Rejeitada', 'Rejeitada')
        ],
        default='Pendente'
    )
    data_candidatura = models.DateField(default=date.today)
    aluno = models.ForeignKey(
        'Aluno',
        on_delete=models.CASCADE,
        related_name='candidaturas_realizadas'
    )
    vaga = models.ForeignKey(
        'VagaMonitoria',
        on_delete=models.CASCADE,
        related_name='candidaturas_recebidas'
    )

    def validarCR(self) -> bool:
        return self.aluno.cr_geral >= 7.0 and self.aluno.cr_disciplina >= 8.0

    def submeter(self):
        self.status = 'Pendente'
        self.save()
        return self

    def cancelar(self):
        self.status = 'Rejeitada'
        self.save()
        return self

    def __str__(self):
        return f"Candidatura de {self.aluno.nome} para {self.vaga.titulo} - {self.status}"


# Registro de uma sessão de monitoria realizada pelo MonitorTEA
class RegistroMonitoria(models.Model):
    data_monitoria = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    horas_trabalhadas = models.DecimalField(max_digits=4, decimal_places=2)
    codigo_disciplina = models.CharField(max_length=20)
    descricao_atividade = models.TextField(help_text="O que foi ensinado/abordado na monitoria")
    alunos_participantes = models.JSONField(
        default=list,
        help_text="Lista de dicionários com 'matricula' e 'nome' dos alunos participantes"
    )
    quantidade_alunos = models.IntegerField(default=0)
    data_registro = models.DateField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)
    
    monitor_tea = models.ForeignKey(
        'MonitorTEA',
        on_delete=models.CASCADE,
        related_name='registros_monitorias'
    )
    candidatura = models.ForeignKey(
        'Candidatura',
        on_delete=models.CASCADE,
        related_name='registros_atividade'
    )

    class Meta:
        verbose_name = 'Registro de Monitoria'
        verbose_name_plural = 'Registros de Monitoria'
        ordering = ['-data_monitoria']

    def submeter(self):
        self.save()
        return self

    def visualizarDetalhes(self):
        return {
            'id': self.id,
            'monitor': str(self.monitor_tea),
            'data_monitoria': self.data_monitoria.isoformat(),
            'horario': f"{self.horario_inicio} - {self.horario_fim}",
            'horas_trabalhadas': float(self.horas_trabalhadas),
            'codigo_disciplina': self.codigo_disciplina,
            'descricao_atividade': self.descricao_atividade,
            'alunos_participantes': self.alunos_participantes,
            'quantidade_alunos': self.quantidade_alunos,
            'observacoes': self.observacoes,
        }

    def __str__(self):
        return f"Monitoria {self.data_monitoria} - {self.monitor_tea.nome} - {self.quantidade_alunos} alunos"
