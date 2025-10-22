from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import date


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=15)
    senha_hash = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def login(self):
        raise NotImplementedError("Método login() deve ser implementado")

    def logout(self):
        raise NotImplementedError("Método logout() deve ser implementado")

    def alterarSenha(self, nova_senha):
        self.senha_hash = make_password(nova_senha)
        self.save()
        return True


class Aluno(Usuario):
    matricula = models.CharField(max_length=12, unique=True, primary_key=True)
    cr_geral = models.FloatField()
    curso = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.matricula} - {self.nome}"

    def matricularEmDisciplina(self, disciplina):
        raise NotImplementedError("Método matricularEmDisciplina() deve ser implementado")

    def buscarMonitoria(self, disciplina):
        return VagaMonitoria.objects.filter(disciplina_obj=disciplina, status='Aberta')

    def realizarCandidatura(self, vaga):
        candidatura = Candidatura.objects.create(
            aluno=self,
            vaga=vaga,
            status='Pendente'
        )
        return candidatura


class Monitor(Aluno):
    cr_disciplina = models.FloatField()

    class Meta:
        verbose_name = 'Monitor'
        verbose_name_plural = 'Monitores'

    def gerenciarDisponibilidade(self):
        raise NotImplementedError("Método gerenciarDisponibilidade() deve ser implementado")

    def visualizarAgenda(self):
        raise NotImplementedError("Método visualizarAgenda() deve ser implementado")

    def submeterRelatorioHoras(self, registro):
        if hasattr(registro, 'submeter'):
            return registro.submeter()
        raise ValueError("Registro inválido")

    def __str__(self):
        return f"Monitor {self.matricula} - {self.nome}"


class MonitorTEA(Monitor):
    salario = models.FloatField()

    class Meta:
        verbose_name = 'Monitor TEA'
        verbose_name_plural = 'Monitores TEA'

    def __str__(self):
        return f"MonitorTEA {self.matricula} - Salário: R$ {self.salario}"


class Professor(Usuario):
    matricula = models.CharField(max_length=12, unique=True, primary_key=True)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return f"{self.matricula} - {self.nome}"


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

    def validarHoras(self, registro):
        registro.status_validacao = 'Aprovado'
        registro.save()
        return registro

    def indicarAlunoParaMonitoria(self, aluno):
        raise NotImplementedError("Método indicarAlunoParaMonitoria() deve ser implementado")

    def __str__(self):
        return f"Coordenador {self.matricula} - {self.nome}"


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


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
        return self.aluno.cr_geral >= 7.0

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


class RegistroAtividadeMonitoria(models.Model):
    descricao_atividade = models.TextField()
    horas_trabalhadas = models.FloatField()
    data_registro = models.DateField(default=date.today)
    status_validacao = models.CharField(
        max_length=20,
        choices=[
            ('Pendente', 'Pendente'),
            ('Aprovado', 'Aprovado'),
            ('Rejeitado', 'Rejeitado')
        ],
        default='Pendente'
    )
    dia = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    
    monitor = models.ForeignKey(
        'Monitor',                 
        on_delete=models.CASCADE,  
        related_name='registros_monitor'
    )
    candidatura = models.ForeignKey(
        'Candidatura',
        on_delete=models.CASCADE,
        related_name='registros_atividade'
    )
    coordenador_validador = models.ForeignKey(
        'Coordenador',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='registros_validados'
    )

    def submeter(self):
        self.status_validacao = 'Pendente'
        self.save()
        return self

    def visualizarDetalhes(self):
        return {
            'id': self.id,
            'monitor': str(self.monitor),
            'descricao_atividade': self.descricao_atividade,
            'horas_trabalhadas': self.horas_trabalhadas,
            'data_registro': self.data_registro.isoformat() if self.data_registro else None,
            'status_validacao': self.status_validacao,
            'dia': self.dia.isoformat() if self.dia else None,
            'observacoes': self.observacoes,
        }

    def aprovar(self):
        self.status_validacao = 'Aprovado'
        self.save()
        return self

    def rejeitar(self):
        self.status_validacao = 'Rejeitado'
        self.save()
        return self

    def __str__(self):
        return f"Registro {self.id} - {self.monitor.nome} - {self.horas_trabalhadas}h"
