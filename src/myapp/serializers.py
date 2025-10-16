from rest_framework import serializers
from myapp.models import Aluno, Professor, Vaga, Candidatura, RegistroMonitoria

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'matricula', 'email', 'telefone', 'cr_geral', 'cr_disciplina', 'curso', 'senha']
        read_only_fields = ['id']
        extra_kwargs = {'senha': {'write_only': True}}

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'nome', 'matricula', 'email', 'telefone', 'senha']
        read_only_fields = ['id']
        extra_kwargs = {'senha': {'write_only': True}}

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = ['id', 'nome', 'pre_requisitos', 'disciplina', 'status', 'prazo_inscricao']

class CandidaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidatura
        fields = ['id', 'aluno', 'vaga', 'documentos', 'status', 'data_candidatura']

class RegistroMonitoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroMonitoria
        fields = ['id', 'aluno', 'vaga', 'horas_trabalhadas', 'data_registro', 'validacao']
