from rest_framework import serializers
from myapp.models import (
    Aluno, Monitor, MonitorTEA, Professor, Coordenador, Casa,
    Disciplina, VagaMonitoria, Candidatura, RegistroMonitoria
)


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ['id', 'nome', 'codigo']
        read_only_fields = ['id']


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['matricula', 'nome', 'email', 'telefone', 'senha_hash', 'cr_geral', 'curso']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }


class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ['matricula', 'nome', 'email', 'telefone', 'senha_hash', 'cr_geral', 'curso']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }


class MonitorTEASerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorTEA
        fields = ['matricula', 'nome', 'email', 'telefone', 'senha_hash', 'cr_geral', 'curso', 'salario']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['cpf', 'nome', 'email', 'telefone', 'senha_hash']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }


class CoordenadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenador
        fields = ['cpf', 'nome', 'email', 'telefone', 'senha_hash']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }


class CasaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casa
        fields = ['id', 'nome', 'email', 'telefone', 'senha_hash']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }
        read_only_fields = ['id']


class VagaMonitoriaSerializer(serializers.ModelSerializer):
    disciplina_detalhes = DisciplinaSerializer(source='disciplina', read_only=True)
    coordenador_detalhes = CoordenadorSerializer(source='coordenador', read_only=True)
    tipo_monitoria_display = serializers.CharField(source='get_tipo_monitoria_display', read_only=True)
    
    class Meta:
        model = VagaMonitoria
        fields = [
            'id', 'titulo', 'pre_requisitos', 'disciplina', 'disciplina_detalhes',
            'coordenador', 'coordenador_detalhes', 'status', 'tipo_monitoria', 
            'tipo_monitoria_display', 'prazo_inscricao'
        ]
        read_only_fields = ['id']


class CandidaturaSerializer(serializers.ModelSerializer):
    aluno_detalhes = AlunoSerializer(source='aluno', read_only=True)
    vaga_detalhes = VagaMonitoriaSerializer(source='vaga', read_only=True)
    
    class Meta:
        model = Candidatura
        fields = [
            'id', 'aluno', 'aluno_detalhes', 'vaga', 'vaga_detalhes',
            'documentos', 'cr_disciplina', 'status', 'data_candidatura'
        ]
        read_only_fields = ['id', 'data_candidatura']


class RegistroMonitoriaSerializer(serializers.ModelSerializer):
    monitor_tea_detalhes = MonitorTEASerializer(source='monitor_tea', read_only=True)
    candidatura_detalhes = CandidaturaSerializer(source='candidatura', read_only=True)

    class Meta:
        model = RegistroMonitoria
        fields = [
            'id', 'monitor_tea', 'monitor_tea_detalhes', 'candidatura', 'candidatura_detalhes',
            'data_monitoria', 'horario_inicio', 'horario_fim', 'horas_trabalhadas',
            'codigo_disciplina', 'descricao_atividade', 'alunos_participantes', 'quantidade_alunos',
            'data_registro', 'observacoes'
        ]
        read_only_fields = ['id', 'data_registro']
