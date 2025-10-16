from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from myapp.models import Aluno, Professor, Vaga, Candidatura, RegistroMonitoria
from myapp.serializers import (
    AlunoSerializer,
    ProfessorSerializer,
    VagaSerializer,
    CandidaturaSerializer,
    RegistroMonitoriaSerializer
)

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class VagaViewSet(viewsets.ModelViewSet):
    queryset = Vaga.objects.all()
    serializer_class = VagaSerializer

class CandidaturaViewSet(viewsets.ModelViewSet):
    queryset = Candidatura.objects.all()
    serializer_class = CandidaturaSerializer

class RegistroMonitoriaViewSet(viewsets.ModelViewSet):
    queryset = RegistroMonitoria.objects.all()
    serializer_class = RegistroMonitoriaSerializer
