from django.db import models
from datetime import date
    
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=12, unique=True, primary_key=True)
    email = models.CharField(max_length=50, unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    cr_geral = models.DecimalField(max_digits=3, decimal_places=1)
    cr_disciplina = models.DecimalField(max_digits=3, decimal_places=1)
    curso = models.CharField(max_length=50)
    senha = models.CharField(max_length=25)

    def __str__(self):
        return self.matricula
    
class Professor(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=12, unique=True, primary_key=True)
    email = models.CharField(max_length=50, unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    senha = models.CharField(max_length=25)

    def __str__(self):
        return self.matricula
    
class Vaga(models.Model):
    nome = models.CharField(max_length=100)
    id = models.IntegerField(unique=True, primary_key=True)
    pre_requisitos = models.TextField()
    disciplina = models.CharField(max_length=40)
    status = models.CharField(max_length=20)
    prazo_inscricao = models.DateField()

    def __str__(self):
        return f"{self.nome} (ID {self.id})"

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

    def __str__(self):
        return f"Candidatura de {self.aluno} para {self.vaga} - {self.status}"

    
class RegistroMonitoria(models.Model):
    horas_trabalhadas = models.DecimalField(max_digits=4, decimal_places=2)
    data_registro = models.DateField()
    validacao = models.BooleanField()
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
    def __str__(self):
        return f"{self.nome} (ID {self.id})"
