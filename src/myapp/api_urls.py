from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.api import (
    AlunoViewSet,
    ProfessorViewSet,
    VagaViewSet,
    CandidaturaViewSet,
    RegistroMonitoriaViewSet
)

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'professores', ProfessorViewSet, basename='professor')
router.register(r'vagas', VagaViewSet, basename='vaga')
router.register(r'candidaturas', CandidaturaViewSet, basename='candidatura')
router.register(r'registros-monitoria', RegistroMonitoriaViewSet, basename='registro-monitoria')

urlpatterns = [
    path('', include(router.urls)),
]
