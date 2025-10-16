from django.db import models
from datetime import date


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    senha = models.CharField(max_length=25)

    class Meta:
        abstract = True

    def login(self):
        raise NotImplementedError("Método login() deve ser implementado")

    def logout(self):
        raise NotImplementedError("Método logout() deve ser implementado")

    def alterarSenha(self, nova_senha):
        self.senha = nova_senha
        self.save()
        return True


class Aluno(Usuario):
    matricula = models.CharField(max_length=12, unique=True, primary_key=True)
    cr_geral = models.DecimalField(max_digits=3, decimal_places=1)
    cr_disciplina = models.DecimalField(max_digits=3, decimal_places=1)
    curso = models.CharField(max_length=50)

    def __str__(self):
        return self.matricula

    def matricularEmDisciplina(self, disciplina):
        raise NotImplementedError("Método matricularEmDisciplina() deve ser implementado")

    def buscarMonitoria(self, disciplina):
        return Vaga.objects.filter(disciplina_obj=disciplina, status='aberta')

    def realizarCandidatura(self, vaga):
        candidatura = Candidatura.objects.create(
            aluno=self,
            vaga=vaga,
            status='pendente'
        )
        return candidatura


class Monitor(Aluno):
    class Meta:
        proxy = True
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


class MonitorTEA(Aluno):
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Monitor TEA'
        verbose_name_plural = 'Monitores TEA'

    def gerenciarDisponibilidade(self):
        raise NotImplementedError("Método gerenciarDisponibilidade() deve ser implementado")

    def visualizarAgenda(self):
        raise NotImplementedError("Método visualizarAgenda() deve ser implementado")

    def submeterRelatorioHoras(self, registro):
        if hasattr(registro, 'submeter'):
            return registro.submeter()
        raise ValueError("Registro inválido")

    def __str__(self):
        return f"MonitorTEA {self.matricula} - Salário: R$ {self.salario}"


class Professor(Usuario):
    matricula = models.CharField(max_length=12, unique=True, primary_key=True)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.matricula

    def cadastrarVaga(self, vaga):
        vaga.save()
        return vaga

    def aprovarCandidatura(self, candidatura):
        candidatura.status = 'aprovada'
        candidatura.save()
        return candidatura

    def validarHoras(self, registro):
        registro.validacao = True
        registro.save()
        return registro

    def indicarAlunoParaMonitoria(self, aluno):
        raise NotImplementedError("Método indicarAlunoParaMonitoria() deve ser implementado")


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Vaga(models.Model):
    nome = models.CharField(max_length=100)
    id = models.IntegerField(unique=True, primary_key=True)
    pre_requisitos = models.TextField()
    disciplina = models.CharField(max_length=40)
    disciplina_obj = models.ForeignKey(
        'Disciplina',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='vagas'
    )
    professor = models.ForeignKey(
        'Professor',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='vagas_cadastradas'
    )
    status = models.CharField(max_length=20)
    prazo_inscricao = models.DateField()

    def __str__(self):
        return f"{self.nome} (ID {self.id})"

    def verDetalhes(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'pre_requisitos': self.pre_requisitos,
            'disciplina': self.disciplina,
            'status': self.status,
            'prazo_inscricao': self.prazo_inscricao.isoformat() if self.prazo_inscricao else None,
        }

    def visualizarCandidaturas(self):
        return self.candidaturas_recebidas.all()


VagaMonitoria = Vaga


class Candidatura(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    documentos = models.FileField()
    status = models.CharField(max_length=20)
    data_candidatura = models.DateField(default=date.today)
    aluno = models.ForeignKey(
        'Aluno',                 
        on_delete=models.CASCADE,  
        related_name='candidaturas_realizadas'
    )
    vaga = models.ForeignKey(
        'Vaga',                  
        on_delete=models.CASCADE, 
        related_name='candidaturas_recebidas'
    )

    def validarCRgeral(self) -> bool:
        return self.aluno.cr_geral >= 7.0
    
    def validarCRdisciplina(self) -> bool:
        return self.aluno.cr_disciplina >= 8.0

    def validarCR(self) -> bool:
        return self.validarCRgeral() and self.validarCRdisciplina()

    def submeter(self):
        self.status = 'submetida'
        self.save()
        return self

    def cancelar(self):
        self.status = 'cancelada'
        self.save()
        return self

    def __str__(self):
        return f"Candidatura de {self.aluno} para {self.vaga} - {self.status}"


class RegistroMonitoria(models.Model):
    horas_trabalhadas = models.DecimalField(max_digits=4, decimal_places=2)
    data_registro = models.DateField()
    validacao = models.BooleanField(default=False)
    codigo_disciplina = models.CharField(max_length=20)
    dia = models.DateField()
    matricula_aluno = models.CharField(max_length=12)
    nome_aluno = models.CharField(max_length=100)
    aluno = models.ForeignKey(
        'Aluno',                 
        on_delete=models.CASCADE,  
        related_name='registros_alunos'
    )
    vaga = models.ForeignKey(
        'Vaga',                  
        on_delete=models.CASCADE, 
        related_name='registros_vaga'
    )
    candidatura = models.ForeignKey(
        'Candidatura',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='registros_atividade'
    )
    professor_validador = models.ForeignKey(
        'Professor',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='registros_validados'
    )

    def submeter(self):
        self.save()
        return self

    def visualizarDetalhes(self):
        return {
            'id': self.id,
            'aluno': str(self.aluno),
            'vaga': str(self.vaga),
            'horas_trabalhadas': float(self.horas_trabalhadas),
            'data_registro': self.data_registro.isoformat() if self.data_registro else None,
            'validacao': self.validacao,
            'codigo_disciplina': self.codigo_disciplina,
            'dia': self.dia.isoformat() if self.dia else None,
            'matricula_aluno': self.matricula_aluno,
            'nome_aluno': self.nome_aluno,
        }

    def __str__(self):
        return f"Registro {self.id} - {self.aluno} - {self.horas_trabalhadas}h"


RegistroAtividadeMonitoria = RegistroMonitoria
