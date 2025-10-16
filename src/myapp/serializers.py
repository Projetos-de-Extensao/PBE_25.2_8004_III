from rest_framework import serializers
from myapp.models import Usuario, Aluno, Monitor, MonitorTEA, Professor, Vaga, Candidatura, RegistroMonitoria



class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['matricula', 'nome', 'email', 'telefone', 'senha', 'cr_geral', 'cr_disciplina', 'curso']
        extra_kwargs = {
            'senha': {'write_only': True}
        }


# class Monitor(serializers.ModelSerializer):
#     class Meta:

# class MonitorTEA(serializers.ModelSerializer):
#     class Meta:
#         model = MonitorTEA
#         fields = ['salario']
#         read_only_fields = ['id']
#         extra_kwargs = {'senha': {'write_only': True}}


# class DisciplinaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Disciplina
#         fields = ['id', 'nome', 'codigo']
#         read_only_fields = ['id']


# class ProfessorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Professor
#         fields = ['cpf']
#         read_only_fields = ['id']
#         extra_kwargs = {'senha': {'write_only': True}}

# class VagaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vaga
#         fields = ['id', 'nome', 'pre_requisitos', 'disciplina', 'status', 'prazo_inscricao']

# class CandidaturaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Candidatura
#         fields = ['id', 'aluno', 'vaga', 'documentos', 'status', 'data_candidatura']

# class RegistroMonitoriaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RegistroMonitoria
#         fields = ['id', 'aluno', 'vaga', 'horas_trabalhadas', 'data_registro', 'validacao']
