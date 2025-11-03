from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from myapp.models import (
    Aluno, Monitor, MonitorTEA, Professor, Coordenador,
    Disciplina, VagaMonitoria, Candidatura, RegistroMonitoria
)
from myapp.serializers import (
    AlunoSerializer, MonitorSerializer, MonitorTEASerializer,
    ProfessorSerializer, CoordenadorSerializer, DisciplinaSerializer,
    VagaMonitoriaSerializer, CandidaturaSerializer, RegistroMonitoriaSerializer
)



class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer


class MonitorTEAViewSet(viewsets.ModelViewSet):
    queryset = MonitorTEA.objects.all()
    serializer_class = MonitorTEASerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class CoordenadorViewSet(viewsets.ModelViewSet):
    queryset = Coordenador.objects.all()
    serializer_class = CoordenadorSerializer


class VagaMonitoriaViewSet(viewsets.ModelViewSet):
    queryset = VagaMonitoria.objects.all()
    serializer_class = VagaMonitoriaSerializer


class CandidaturaViewSet(viewsets.ModelViewSet):
    queryset = Candidatura.objects.all()
    serializer_class = CandidaturaSerializer


class RegistroMonitoriaViewSet(viewsets.ModelViewSet):
    queryset = RegistroMonitoria.objects.all()
    serializer_class = RegistroMonitoriaSerializer

