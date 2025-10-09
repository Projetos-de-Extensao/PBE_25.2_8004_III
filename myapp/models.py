from django.db import models
    
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=12, unique=True)
    email = models.CharField(max_length=50, unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    cr_geral = models.DecimalField(max_digits=2, decimal_places=1)
    cr_disciplina = models.DecimalField(max_digits=3, decimal_places=1)
    curso = models.CharField(max_length=50)
    senha = models.CharField(max_length=25)

    def __str__(self):
        return self.matricula
    
class Professor(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=12, unique=True)
    email = models.CharField(max_length=50, unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    senha = models.CharField(max_length=25)

    def __str__(self):
        return self.matricula
    
class Vaga(models.Model):
    nome = models.CharField(max_length=100)
    id = models.IntegerField(max_length=3, unique=True)
    pre_requisitos = models.TextField()
    disciplina = models.CharField(max_length=40)
    status = models.CharField(max_length=20)
    prazo_inscricao = models.DateField()

    def __str__(self):
        return self.id
    
class Candidatura(models.Model):
    id = models.IntegerField(max_length=3, unique=True)
    # aluno =  // será substituído por conta do relacionamento
    # vaga =  // será substituído por conta do relacionamento
    documentos = models.FileField()
    status = models.CharField(max_length=20)
    data_candidatura = models.DateField()

    def __str__(self):
        return self.id
    
class RegistroMonitoria(models.Model):
    id = models.IntegerField(max_length=3, unique=True)
    # aluno =  // será substituído por conta do relacionamento
    # vaga =  // será substituído por conta do relacionamento
    horas_trabalhadas = models.DecimalField(max_digits=4, decimal_places=2)
    data_registro = models.DateField()
    validacao = models.BooleanField()

    def __str__(self):
        return self.id