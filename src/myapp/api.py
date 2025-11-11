from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
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
    permission_classes = [AllowAny]


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [AllowAny]


class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    permission_classes = [AllowAny]


class MonitorTEAViewSet(viewsets.ModelViewSet):
    queryset = MonitorTEA.objects.all()
    serializer_class = MonitorTEASerializer
    permission_classes = [AllowAny]


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [AllowAny]


class CoordenadorViewSet(viewsets.ModelViewSet):
    queryset = Coordenador.objects.all()
    serializer_class = CoordenadorSerializer
    permission_classes = [AllowAny]


class VagaMonitoriaViewSet(viewsets.ModelViewSet):
    queryset = VagaMonitoria.objects.all()
    serializer_class = VagaMonitoriaSerializer
    permission_classes = [AllowAny]


class CandidaturaViewSet(viewsets.ModelViewSet):
    queryset = Candidatura.objects.all()
    serializer_class = CandidaturaSerializer
    permission_classes = [AllowAny]


class RegistroMonitoriaViewSet(viewsets.ModelViewSet):
    queryset = RegistroMonitoria.objects.all()
    serializer_class = RegistroMonitoriaSerializer
    permission_classes = [AllowAny]

