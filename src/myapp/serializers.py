from rest_framework import serializers
from myapp.models import (
    Aluno, Monitor, MonitorTEA, Professor, Coordenador,
    Disciplina, VagaMonitoria, Candidatura, RegistroAtividadeMonitoria
)

# models -> serializer -> url -> view
# Models → Define a estrutura de dados (tabelas do banco)
# Serializers → Converte modelos em JSON e valida dados
# Views → Lógica de negócio e controle das requisições
# URLs → Define as rotas/endpoints da API

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
        fields = ['matricula', 'nome', 'email', 'telefone', 'senha_hash', 'cr_geral', 'curso', 'cr_disciplina']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }


class MonitorTEASerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorTEA
        fields = ['matricula', 'nome', 'email', 'telefone', 'senha_hash', 'cr_geral', 'curso', 'cr_disciplina', 'salario']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['matricula', 'nome', 'email', 'telefone', 'senha_hash', 'cpf']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }


class CoordenadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenador
        fields = ['matricula', 'nome', 'email', 'telefone', 'senha_hash', 'cpf']
        extra_kwargs = {
            'senha_hash': {'write_only': True}
        }


class VagaMonitoriaSerializer(serializers.ModelSerializer):
    disciplina_detalhes = DisciplinaSerializer(source='disciplina', read_only=True)
    coordenador_detalhes = CoordenadorSerializer(source='coordenador', read_only=True)
    
    class Meta:
        model = VagaMonitoria
        fields = [
            'id', 'titulo', 'pre_requisitos', 'disciplina', 'disciplina_detalhes',
            'coordenador', 'coordenador_detalhes', 'status', 'prazo_inscricao'
        ]
        read_only_fields = ['id']


class CandidaturaSerializer(serializers.ModelSerializer):
    aluno_detalhes = AlunoSerializer(source='aluno', read_only=True)
    vaga_detalhes = VagaMonitoriaSerializer(source='vaga', read_only=True)
    
    class Meta:
        model = Candidatura
        fields = [
            'id', 'aluno', 'aluno_detalhes', 'vaga', 'vaga_detalhes',
            'documentos', 'status', 'data_candidatura'
        ]
        read_only_fields = ['id', 'data_candidatura']


class RegistroAtividadeMonitoriaSerializer(serializers.ModelSerializer):
    monitor_detalhes = MonitorSerializer(source='monitor', read_only=True)
    candidatura_detalhes = CandidaturaSerializer(source='candidatura', read_only=True)
    coordenador_validador_detalhes = CoordenadorSerializer(source='coordenador_validador', read_only=True)
    
    class Meta:
        model = RegistroAtividadeMonitoria
        fields = [
            'id', 'monitor', 'monitor_detalhes', 'candidatura', 'candidatura_detalhes',
            'coordenador_validador', 'coordenador_validador_detalhes',
            'descricao_atividade', 'horas_trabalhadas', 'data_registro',
            'status_validacao', 'dia', 'observacoes'
        ]
        read_only_fields = ['id', 'data_registro']
