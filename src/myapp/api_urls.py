from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.api import (
    AlunoViewSet, MonitorViewSet, MonitorTEAViewSet,
    ProfessorViewSet, CoordenadorViewSet, DisciplinaViewSet,
    VagaMonitoriaViewSet, CandidaturaViewSet, RegistroAtividadeMonitoriaViewSet
)

router = DefaultRouter()
router.register(r'disciplinas', DisciplinaViewSet, basename='disciplina')
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'monitores', MonitorViewSet, basename='monitor')
router.register(r'monitores-tea', MonitorTEAViewSet, basename='monitor-tea')
router.register(r'professores', ProfessorViewSet, basename='professor')
router.register(r'coordenadores', CoordenadorViewSet, basename='coordenador')
router.register(r'vagas-monitoria', VagaMonitoriaViewSet, basename='vaga-monitoria')
router.register(r'candidaturas', CandidaturaViewSet, basename='candidatura')
router.register(r'registros-atividade', RegistroAtividadeMonitoriaViewSet, basename='registro-atividade')

urlpatterns = [
    path('', include(router.urls)),
]
