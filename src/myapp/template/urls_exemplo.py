from django.urls import path
from myapp import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Cadastros
    path('cadastro/aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/professor/', views.cadastro_professor, name='cadastro_professor'),
    
    # Vagas
    path('vagas/', views.lista_vagas, name='lista_vagas'),
    path('vagas/cadastrar/', views.cadastro_vaga, name='cadastro_vaga'),
    path('vagas/<int:vaga_id>/', views.detalhes_vaga, name='detalhes_vaga'),
    path('vagas/<int:vaga_id>/candidatar/', views.candidatar_vaga, name='candidatar_vaga'),
    path('vagas/<int:vaga_id>/editar/', views.editar_vaga, name='editar_vaga'),
    path('vagas/<int:vaga_id>/candidaturas/', views.candidaturas_vaga, name='candidaturas_vaga'),
    
    # Monitor
    path('monitor/painel/', views.painel_monitor, name='painel_monitor'),
    path('monitor/registrar/', views.registrar_monitoria, name='registrar_monitoria'),
    
    # Coordenador
    path('coordenador/painel/', views.painel_coordenador, name='painel_coordenador'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Candidaturas
    path('candidaturas/<int:candidatura_id>/', views.detalhes_candidatura, name='detalhes_candidatura'),
    path('candidaturas/<int:candidatura_id>/aprovar/', views.aprovar_candidatura, name='aprovar_candidatura'),
    path('candidaturas/<int:candidatura_id>/rejeitar/', views.rejeitar_candidatura, name='rejeitar_candidatura'),
    
    # Monitores
    path('monitores/<str:matricula>/', views.detalhes_monitor, name='detalhes_monitor'),
]
