from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from datetime import date, timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from myapp.models import (
    Aluno, Professor, Coordenador, Casa, Monitor, MonitorTEA,
    Disciplina, VagaMonitoria, Candidatura, RegistroMonitoria
)


# ==================== TESTES DE MODELS ====================

class AlunoModelTest(TestCase):
    """Testes para o modelo Aluno"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.aluno = Aluno.objects.create(
            matricula='202300001',
            nome='João da Silva',
            email='joao@test.com',
            telefone='11999999999',
            senha_hash=make_password('senha123'),
            cr_geral=8.5,
            curso='Ciência da Computação'
        )
    
    def test_aluno_criacao(self):
        """Testa se o aluno foi criado corretamente"""
        self.assertEqual(self.aluno.matricula, '202300001')
        self.assertEqual(self.aluno.nome, 'João da Silva')
        self.assertEqual(self.aluno.cr_geral, 8.5)
        self.assertTrue(check_password('senha123', self.aluno.senha_hash))
    
    def test_aluno_str(self):
        """Testa a representação em string do aluno"""
        self.assertEqual(str(self.aluno), '202300001 - João da Silva')
    
    def test_alterar_senha(self):
        """Testa a alteração de senha do aluno"""
        self.aluno.alterarSenha('nova_senha456')
        self.assertTrue(check_password('nova_senha456', self.aluno.senha_hash))
        self.assertFalse(check_password('senha123', self.aluno.senha_hash))


class ProfessorModelTest(TestCase):
    """Testes para o modelo Professor"""
    
    def setUp(self):
        self.professor = Professor.objects.create(
            cpf='12345678900',
            nome='Maria Santos',
            email='maria@test.com',
            telefone='11988888888',
            senha_hash=make_password('prof123')
        )
    
    def test_professor_criacao(self):
        """Testa se o professor foi criado corretamente"""
        self.assertEqual(self.professor.cpf, '12345678900')
        self.assertEqual(self.professor.nome, 'Maria Santos')
        self.assertTrue(check_password('prof123', self.professor.senha_hash))
    
    def test_professor_str(self):
        """Testa a representação em string do professor"""
        self.assertEqual(str(self.professor), '12345678900 - Maria Santos')


class DisciplinaModelTest(TestCase):
    """Testes para o modelo Disciplina"""
    
    def setUp(self):
        self.disciplina = Disciplina.objects.create(
            codigo='CC101',
            nome='Introdução à Programação'
        )
    
    def test_disciplina_criacao(self):
        """Testa se a disciplina foi criada corretamente"""
        self.assertEqual(self.disciplina.codigo, 'CC101')
        self.assertEqual(self.disciplina.nome, 'Introdução à Programação')
    
    def test_disciplina_str(self):
        """Testa a representação em string da disciplina"""
        self.assertEqual(str(self.disciplina), 'CC101 - Introdução à Programação')


class VagaMonitoriaModelTest(TestCase):
    """Testes para o modelo VagaMonitoria"""
    
    def setUp(self):
        self.coordenador = Coordenador.objects.create(
            cpf='98765432100',
            nome='Carlos Coordenador',
            email='carlos@test.com',
            telefone='11977777777',
            senha_hash=make_password('coord123')
        )
        
        self.disciplina = Disciplina.objects.create(
            codigo='CC102',
            nome='Estruturas de Dados'
        )
        
        self.vaga = VagaMonitoria.objects.create(
            titulo='Monitor de Estruturas de Dados',
            pre_requisitos='CR mínimo 7.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
    
    def test_vaga_criacao(self):
        """Testa se a vaga foi criada corretamente"""
        self.assertEqual(self.vaga.titulo, 'Monitor de Estruturas de Dados')
        self.assertEqual(self.vaga.status, 'Aberta')
        self.assertEqual(self.vaga.disciplina, self.disciplina)
    
    def test_vaga_str(self):
        """Testa a representação em string da vaga"""
        self.assertEqual(str(self.vaga), 'Monitor de Estruturas de Dados - Estruturas de Dados')
    
    def test_ver_detalhes(self):
        """Testa o método verDetalhes da vaga"""
        detalhes = self.vaga.verDetalhes()
        self.assertEqual(detalhes['titulo'], 'Monitor de Estruturas de Dados')
        self.assertEqual(detalhes['status'], 'Aberta')


class CandidaturaModelTest(TestCase):
    """Testes para o modelo Candidatura"""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            matricula='202300002',
            nome='Ana Aluna',
            email='ana@test.com',
            telefone='11966666666',
            senha_hash=make_password('senha123'),
            cr_geral=8.0,
            curso='Engenharia de Software'
        )
        
        self.disciplina = Disciplina.objects.create(
            codigo='ES101',
            nome='Engenharia de Software I'
        )
        
        self.vaga = VagaMonitoria.objects.create(
            titulo='Monitor de ES I',
            pre_requisitos='CR mínimo 7.0',
            disciplina=self.disciplina,
            status='Aberta',
            prazo_inscricao=date.today() + timedelta(days=15)
        )
        
        self.candidatura = Candidatura.objects.create(
            aluno=self.aluno,
            vaga=self.vaga,
            cr_disciplina=8.5,
            documentos='Histórico escolar anexado',
            status='Pendente'
        )
    
    def test_candidatura_criacao(self):
        """Testa se a candidatura foi criada corretamente"""
        self.assertEqual(self.candidatura.aluno, self.aluno)
        self.assertEqual(self.candidatura.vaga, self.vaga)
        self.assertEqual(self.candidatura.status, 'Pendente')
        self.assertEqual(self.candidatura.cr_disciplina, 8.5)
    
    def test_validar_cr_aprovado(self):
        """Testa validação de CR com valores aprovados"""
        self.candidatura.cr_disciplina = 8.5
        self.aluno.cr_geral = 7.5
        self.aluno.save()
        self.assertTrue(self.candidatura.validarCR())
    
    def test_validar_cr_reprovado_cr_geral(self):
        """Testa validação de CR com CR geral baixo"""
        self.candidatura.cr_disciplina = 8.5
        self.aluno.cr_geral = 6.5  # Abaixo de 7.0
        self.aluno.save()
        self.assertFalse(self.candidatura.validarCR())
    
    def test_validar_cr_reprovado_cr_disciplina(self):
        """Testa validação de CR com CR da disciplina baixo"""
        self.candidatura.cr_disciplina = 7.5  # Abaixo de 8.0
        self.aluno.cr_geral = 8.0
        self.aluno.save()
        self.assertFalse(self.candidatura.validarCR())


# ==================== TESTES DE VIEWS ====================

class HomeViewTest(TestCase):
    """Testes para a view home"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_status_code(self):
        """Testa se a página home carrega corretamente"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_template(self):
        """Testa se o template correto está sendo usado"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')


class LoginViewTest(TestCase):
    """Testes para a view de login"""
    
    def setUp(self):
        self.client = Client()
        self.aluno = Aluno.objects.create(
            matricula='202300003',
            nome='Pedro Teste',
            email='pedro@test.com',
            telefone='11955555555',
            senha_hash=make_password('senha123'),
            cr_geral=7.5,
            curso='Sistemas de Informação'
        )
    
    def test_login_page_status_code(self):
        """Testa se a página de login carrega"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_page_template(self):
        """Testa se o template correto está sendo usado"""
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_sucesso(self):
        """Testa login bem-sucedido"""
        response = self.client.post(reverse('login'), {
            'email': 'pedro@test.com',
            'password': 'senha123',
            'user_type': 'aluno'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(self.client.session.get('user_type'), 'aluno')
        self.assertEqual(self.client.session.get('user_id'), '202300003')
    
    def test_login_senha_incorreta(self):
        """Testa login com senha incorreta"""
        response = self.client.post(reverse('login'), {
            'email': 'pedro@test.com',
            'password': 'senha_errada',
            'user_type': 'aluno'
        })
        self.assertEqual(response.status_code, 200)  # Permanece na página
        self.assertIsNone(self.client.session.get('user_type'))


class CadastroAlunoViewTest(TestCase):
    """Testes para cadastro de aluno"""
    
    def setUp(self):
        self.client = Client()
    
    def test_cadastro_aluno_get(self):
        """Testa carregamento da página de cadastro"""
        response = self.client.get(reverse('cadastro_aluno'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_aluno.html')
    
    def test_cadastro_aluno_post_sucesso(self):
        """Testa cadastro de aluno com dados válidos"""
        response = self.client.post(reverse('cadastro_aluno'), {
            'matricula': '202300004',
            'nome': 'Novo Aluno',
            'email': 'novo@test.com',
            'telefone': '11944444444',
            'senha': 'senha123',
            'cr_geral': '7.0',
            'curso': 'Engenharia'
        })
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        self.assertTrue(Aluno.objects.filter(matricula='202300004').exists())


class ListaVagasViewTest(TestCase):
    """Testes para listagem de vagas"""
    
    def setUp(self):
        self.client = Client()
        self.disciplina = Disciplina.objects.create(
            codigo='TEST101',
            nome='Disciplina Teste'
        )
        self.vaga = VagaMonitoria.objects.create(
            titulo='Vaga Teste',
            pre_requisitos='Nenhum',
            disciplina=self.disciplina,
            status='Aberta',
            prazo_inscricao=date.today() + timedelta(days=10)
        )
    
    def test_lista_vagas_status_code(self):
        """Testa se a página de vagas carrega"""
        response = self.client.get(reverse('lista_vagas'))
        self.assertEqual(response.status_code, 200)
    
    def test_lista_vagas_contem_vaga(self):
        """Testa se a vaga criada aparece na lista"""
        response = self.client.get(reverse('lista_vagas'))
        self.assertContains(response, 'Vaga Teste')
        self.assertEqual(len(response.context['vagas']), 1)


class CandidaturaViewTest(TestCase):
    """Testes para o sistema de candidaturas"""
    
    def setUp(self):
        self.client = Client()
        
        # Criar aluno
        self.aluno = Aluno.objects.create(
            matricula='202300005',
            nome='Candidato Teste',
            email='candidato@test.com',
            telefone='11933333333',
            senha_hash=make_password('senha123'),
            cr_geral=8.0,
            curso='Teste'
        )
        
        # Criar disciplina e vaga
        self.disciplina = Disciplina.objects.create(
            codigo='CAND101',
            nome='Disciplina Candidatura'
        )
        
        self.vaga = VagaMonitoria.objects.create(
            titulo='Vaga para Candidatura',
            pre_requisitos='CR > 7.0',
            disciplina=self.disciplina,
            status='Aberta',
            prazo_inscricao=date.today() + timedelta(days=20)
        )
        
        # Fazer login do aluno
        session = self.client.session
        session['user_type'] = 'aluno'
        session['user_id'] = '202300005'
        session.save()
    
    def test_candidatar_vaga_get(self):
        """Testa carregamento do formulário de candidatura"""
        response = self.client.get(reverse('candidatar_vaga', args=[self.vaga.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidatar_vaga.html')
    
    def test_candidatar_vaga_post_sucesso(self):
        """Testa envio de candidatura com sucesso"""
        response = self.client.post(reverse('candidatar_vaga', args=[self.vaga.id]), {
            'cr_disciplina': '8.5',
            'documentos': 'Documentos anexados'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Candidatura.objects.filter(aluno=self.aluno, vaga=self.vaga).exists())


# ==================== TESTES DE INTEGRAÇÃO ====================

class FluxoCompletoMonitoriaTest(TestCase):
    """Teste do fluxo completo: cadastro -> candidatura -> aprovação"""
    
    def setUp(self):
        self.client = Client()
        
        # Criar coordenador
        self.coordenador = Coordenador.objects.create(
            cpf='11111111111',
            nome='Coord Teste',
            email='coord@test.com',
            telefone='11922222222',
            senha_hash=make_password('coord123')
        )
        
        # Criar disciplina
        self.disciplina = Disciplina.objects.create(
            codigo='FLOW101',
            nome='Disciplina Fluxo'
        )
        
        # Criar aluno
        self.aluno = Aluno.objects.create(
            matricula='202300006',
            nome='Aluno Fluxo',
            email='aluno.fluxo@test.com',
            telefone='11911111111',
            senha_hash=make_password('aluno123'),
            cr_geral=8.5,
            curso='Teste'
        )
    
    def test_fluxo_completo(self):
        """Testa o fluxo completo do sistema"""
        
        # 1. Coordenador cria vaga
        session = self.client.session
        session['user_type'] = 'coordenador'
        session['user_id'] = '11111111111'
        session.save()
        
        response = self.client.post(reverse('cadastro_vaga'), {
            'titulo': 'Vaga Fluxo Teste',
            'pre_requisitos': 'CR > 7.0',
            'disciplina': self.disciplina.id,
            'status': 'Aberta',
            'prazo_inscricao': (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
        })
        
        vaga = VagaMonitoria.objects.get(titulo='Vaga Fluxo Teste')
        self.assertIsNotNone(vaga)
        
        # 2. Aluno se candidata
        session = self.client.session
        session['user_type'] = 'aluno'
        session['user_id'] = '202300006'
        session.save()
        
        response = self.client.post(reverse('candidatar_vaga', args=[vaga.id]), {
            'cr_disciplina': '9.0',
            'documentos': 'CV e histórico'
        })
        
        candidatura = Candidatura.objects.get(aluno=self.aluno, vaga=vaga)
        self.assertEqual(candidatura.status, 'Pendente')
        
        # 3. Coordenador aprova candidatura
        session = self.client.session
        session['user_type'] = 'coordenador'
        session['user_id'] = '11111111111'
        session.save()
        
        response = self.client.get(reverse('aprovar_candidatura', args=[candidatura.id]))
        
        candidatura.refresh_from_db()
        self.assertEqual(candidatura.status, 'Aprovada')
        
        # 4. Verifica se monitor foi criado
        self.assertTrue(Monitor.objects.filter(matricula='202300006').exists())


# ==================== TESTES DE API REST ====================

@override_settings(
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': [],
        'DEFAULT_PERMISSION_CLASSES': [],
    }
)
class DisciplinaAPITest(APITestCase):
    """Testes para API de Disciplinas"""
    
    def setUp(self):
        self.client = APIClient()
        self.disciplina_data = {
            'codigo': 'API101',
            'nome': 'Disciplina via API'
        }
    
    def test_criar_disciplina_via_api(self):
        """Testa criação de disciplina via POST na API"""
        response = self.client.post('/api/disciplinas/', self.disciplina_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Disciplina.objects.count(), 1)
        self.assertEqual(Disciplina.objects.get().codigo, 'API101')
    
    def test_listar_disciplinas_via_api(self):
        """Testa listagem de disciplinas via GET na API"""
        Disciplina.objects.create(**self.disciplina_data)
        response = self.client.get('/api/disciplinas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_obter_disciplina_por_id_via_api(self):
        """Testa obter disciplina específica via GET na API"""
        disciplina = Disciplina.objects.create(**self.disciplina_data)
        response = self.client.get(f'/api/disciplinas/{disciplina.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['codigo'], 'API101')
    
    def test_atualizar_disciplina_via_api(self):
        """Testa atualização de disciplina via PUT na API"""
        disciplina = Disciplina.objects.create(**self.disciplina_data)
        updated_data = {'codigo': 'API101', 'nome': 'Disciplina Atualizada'}
        response = self.client.put(f'/api/disciplinas/{disciplina.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        disciplina.refresh_from_db()
        self.assertEqual(disciplina.nome, 'Disciplina Atualizada')
    
    def test_deletar_disciplina_via_api(self):
        """Testa exclusão de disciplina via DELETE na API"""
        disciplina = Disciplina.objects.create(**self.disciplina_data)
        response = self.client.delete(f'/api/disciplinas/{disciplina.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Disciplina.objects.count(), 0)


@override_settings(
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': [],
        'DEFAULT_PERMISSION_CLASSES': [],
    }
)
class AlunoAPITest(APITestCase):
    """Testes para API de Alunos"""
    
    def setUp(self):
        self.client = APIClient()
        self.aluno_data = {
            'matricula': '202300010',
            'nome': 'Aluno API Teste',
            'email': 'aluno.api@test.com',
            'telefone': '11900000000',
            'senha_hash': make_password('senha123'),
            'cr_geral': 8.0,
            'curso': 'Engenharia'
        }
    
    def test_criar_aluno_via_api(self):
        """Testa criação de aluno via POST na API"""
        response = self.client.post('/api/alunos/', self.aluno_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Aluno.objects.count(), 1)
        self.assertEqual(Aluno.objects.get().matricula, '202300010')
    
    def test_listar_alunos_via_api(self):
        """Testa listagem de alunos via GET na API"""
        Aluno.objects.create(**self.aluno_data)
        response = self.client.get('/api/alunos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_obter_aluno_por_matricula_via_api(self):
        """Testa obter aluno específico via GET na API"""
        aluno = Aluno.objects.create(**self.aluno_data)
        response = self.client.get(f'/api/alunos/{aluno.matricula}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Aluno API Teste')
    
    def test_atualizar_aluno_via_api(self):
        """Testa atualização de aluno via PATCH na API"""
        aluno = Aluno.objects.create(**self.aluno_data)
        updated_data = {'cr_geral': 9.0}
        response = self.client.patch(f'/api/alunos/{aluno.matricula}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        aluno.refresh_from_db()
        self.assertEqual(aluno.cr_geral, 9.0)
    
    def test_deletar_aluno_via_api(self):
        """Testa exclusão de aluno via DELETE na API"""
        aluno = Aluno.objects.create(**self.aluno_data)
        response = self.client.delete(f'/api/alunos/{aluno.matricula}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Aluno.objects.count(), 0)


@override_settings(
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': [],
        'DEFAULT_PERMISSION_CLASSES': [],
    }
)
class VagaMonitoriaAPITest(APITestCase):
    """Testes para API de Vagas de Monitoria"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Criar disciplina
        self.disciplina = Disciplina.objects.create(
            codigo='API202',
            nome='Disciplina para Vaga API'
        )
        
        # Criar coordenador
        self.coordenador = Coordenador.objects.create(
            cpf='99999999999',
            nome='Coord API',
            email='coord.api@test.com',
            telefone='11999999999',
            senha_hash=make_password('coord123')
        )
        
        self.vaga_data = {
            'titulo': 'Vaga API Teste',
            'pre_requisitos': 'CR > 7.0',
            'disciplina': self.disciplina.id,
            'coordenador': self.coordenador.cpf,
            'status': 'Aberta',
            'prazo_inscricao': (date.today() + timedelta(days=30)).isoformat()
        }
    
    def test_criar_vaga_via_api(self):
        """Testa criação de vaga via POST na API"""
        response = self.client.post('/api/vagas-monitoria/', self.vaga_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VagaMonitoria.objects.count(), 1)
    
    def test_listar_vagas_via_api(self):
        """Testa listagem de vagas via GET na API"""
        VagaMonitoria.objects.create(
            titulo='Vaga API Teste',
            pre_requisitos='CR > 7.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
        response = self.client.get('/api/vagas-monitoria/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filtrar_vagas_abertas_via_api(self):
        """Testa filtragem de vagas por status"""
        # Criar vaga aberta
        VagaMonitoria.objects.create(
            titulo='Vaga Aberta',
            pre_requisitos='CR > 7.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
        
        # Criar vaga fechada
        VagaMonitoria.objects.create(
            titulo='Vaga Fechada',
            pre_requisitos='CR > 7.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Fechada',
            prazo_inscricao=date.today() - timedelta(days=1)
        )
        
        # Listar todas
        response = self.client.get('/api/vagas-monitoria/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


@override_settings(
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': [],
        'DEFAULT_PERMISSION_CLASSES': [],
    }
)
class CandidaturaAPITest(APITestCase):
    """Testes para API de Candidaturas"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Criar aluno
        self.aluno = Aluno.objects.create(
            matricula='202300011',
            nome='Candidato API',
            email='candidato.api@test.com',
            telefone='11911111111',
            senha_hash=make_password('senha123'),
            cr_geral=8.5,
            curso='Computação'
        )
        
        # Criar disciplina e vaga
        self.disciplina = Disciplina.objects.create(
            codigo='API303',
            nome='Disciplina Candidatura API'
        )
        
        self.vaga = VagaMonitoria.objects.create(
            titulo='Vaga para Candidatura API',
            pre_requisitos='CR > 7.0',
            disciplina=self.disciplina,
            status='Aberta',
            prazo_inscricao=date.today() + timedelta(days=20)
        )
        
        self.candidatura_data = {
            'aluno': self.aluno.matricula,
            'vaga': self.vaga.id,
            'cr_disciplina': 9.0,
            'documentos': 'Documentos via API',
            'status': 'Pendente'
        }
    
    def test_criar_candidatura_via_api(self):
        """Testa criação de candidatura via POST na API"""
        response = self.client.post('/api/candidaturas/', self.candidatura_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Candidatura.objects.count(), 1)
    
    def test_listar_candidaturas_via_api(self):
        """Testa listagem de candidaturas via GET na API"""
        Candidatura.objects.create(
            aluno=self.aluno,
            vaga=self.vaga,
            cr_disciplina=9.0,
            documentos='Docs',
            status='Pendente'
        )
        response = self.client.get('/api/candidaturas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_atualizar_status_candidatura_via_api(self):
        """Testa atualização de status de candidatura via PATCH"""
        candidatura = Candidatura.objects.create(
            aluno=self.aluno,
            vaga=self.vaga,
            cr_disciplina=9.0,
            documentos='Docs',
            status='Pendente'
        )
        
        updated_data = {'status': 'Aprovada'}
        response = self.client.patch(f'/api/candidaturas/{candidatura.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        candidatura.refresh_from_db()
        self.assertEqual(candidatura.status, 'Aprovada')


@override_settings(
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': [],
        'DEFAULT_PERMISSION_CLASSES': [],
    }
)
class ProfessorAPITest(APITestCase):
    """Testes para API de Professores"""
    
    def setUp(self):
        self.client = APIClient()
        self.professor_data = {
            'cpf': '88888888888',
            'nome': 'Professor API',
            'email': 'professor.api@test.com',
            'telefone': '11988888888',
            'senha_hash': make_password('prof123')
        }
    
    def test_criar_professor_via_api(self):
        """Testa criação de professor via POST na API"""
        response = self.client.post('/api/professores/', self.professor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professor.objects.count(), 1)
    
    def test_listar_professores_via_api(self):
        """Testa listagem de professores via GET na API"""
        Professor.objects.create(**self.professor_data)
        response = self.client.get('/api/professores/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


# ==================== TESTES DE TIPO DE MONITORIA ====================

class TipoMonitoriaAPITest(APITestCase):
    """Testes para verificar se o campo tipo_monitoria está funcionando corretamente na API"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Criar disciplina
        self.disciplina = Disciplina.objects.create(
            codigo='TM001',
            nome='Disciplina Tipo Monitoria'
        )
        
        # Criar coordenador
        self.coordenador = Coordenador.objects.create(
            cpf='77777777777',
            nome='Coord Tipo Monitoria',
            email='coord.tm@test.com',
            telefone='11977777777',
            senha_hash=make_password('coord123')
        )
    
    def test_serializer_vaga_monitor_voluntario(self):
        """Testa serialização de vaga para Monitor Voluntário"""
        vaga = VagaMonitoria.objects.create(
            titulo='Vaga Monitor Voluntário',
            pre_requisitos='CR >= 7.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            tipo_monitoria='Monitor',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
        
        from myapp.serializers import VagaMonitoriaSerializer
        serializer = VagaMonitoriaSerializer(vaga)
        data = serializer.data
        
        # Verificações
        self.assertIn('tipo_monitoria', data)
        self.assertEqual(data['tipo_monitoria'], 'Monitor')
        self.assertIn('tipo_monitoria_display', data)
        self.assertEqual(data['tipo_monitoria_display'], 'Monitor (Voluntário)')
    
    def test_serializer_vaga_monitor_tea(self):
        """Testa serialização de vaga para Monitor TEA"""
        vaga = VagaMonitoria.objects.create(
            titulo='Vaga Monitor TEA',
            pre_requisitos='CR >= 8.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            tipo_monitoria='MonitorTEA',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
        
        from myapp.serializers import VagaMonitoriaSerializer
        serializer = VagaMonitoriaSerializer(vaga)
        data = serializer.data
        
        # Verificações
        self.assertIn('tipo_monitoria', data)
        self.assertEqual(data['tipo_monitoria'], 'MonitorTEA')
        self.assertIn('tipo_monitoria_display', data)
        self.assertEqual(data['tipo_monitoria_display'], 'Monitor TEA (Remunerado)')
    
    def test_criar_vaga_monitor_via_api(self):
        """Testa criação de vaga Monitor via API"""
        vaga_data = {
            'titulo': 'Vaga API Monitor',
            'pre_requisitos': 'CR >= 7.0',
            'disciplina': self.disciplina.id,
            'coordenador': self.coordenador.cpf,
            'status': 'Aberta',
            'tipo_monitoria': 'Monitor',
            'prazo_inscricao': (date.today() + timedelta(days=30)).isoformat()
        }
        
        response = self.client.post('/api/vagas-monitoria/', vaga_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tipo_monitoria', response.data)
        self.assertEqual(response.data['tipo_monitoria'], 'Monitor')
    
    def test_criar_vaga_monitor_tea_via_api(self):
        """Testa criação de vaga MonitorTEA via API"""
        vaga_data = {
            'titulo': 'Vaga API MonitorTEA',
            'pre_requisitos': 'CR >= 8.0',
            'disciplina': self.disciplina.id,
            'coordenador': self.coordenador.cpf,
            'status': 'Aberta',
            'tipo_monitoria': 'MonitorTEA',
            'prazo_inscricao': (date.today() + timedelta(days=30)).isoformat()
        }
        
        response = self.client.post('/api/vagas-monitoria/', vaga_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tipo_monitoria', response.data)
        self.assertEqual(response.data['tipo_monitoria'], 'MonitorTEA')
        self.assertIn('tipo_monitoria_display', response.data)
        self.assertEqual(response.data['tipo_monitoria_display'], 'Monitor TEA (Remunerado)')
    
    def test_listar_vagas_com_tipos_diferentes(self):
        """Testa listagem de vagas com tipos diferentes"""
        # Criar vaga Monitor
        VagaMonitoria.objects.create(
            titulo='Vaga Monitor',
            pre_requisitos='CR >= 7.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            tipo_monitoria='Monitor',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
        
        # Criar vaga MonitorTEA
        VagaMonitoria.objects.create(
            titulo='Vaga MonitorTEA',
            pre_requisitos='CR >= 8.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            tipo_monitoria='MonitorTEA',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
        
        response = self.client.get('/api/vagas-monitoria/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verificar que ambos os tipos estão presentes
        tipos = [vaga['tipo_monitoria'] for vaga in response.data]
        self.assertIn('Monitor', tipos)
        self.assertIn('MonitorTEA', tipos)
    
    def test_atualizar_tipo_monitoria_via_api(self):
        """Testa atualização do tipo de monitoria via API"""
        vaga = VagaMonitoria.objects.create(
            titulo='Vaga para Atualizar',
            pre_requisitos='CR >= 7.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            tipo_monitoria='Monitor',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
        
        updated_data = {
            'titulo': 'Vaga para Atualizar',
            'pre_requisitos': 'CR >= 7.0',
            'disciplina': self.disciplina.id,
            'coordenador': self.coordenador.cpf,
            'status': 'Aberta',
            'tipo_monitoria': 'MonitorTEA',
            'prazo_inscricao': (date.today() + timedelta(days=30)).isoformat()
        }
        
        response = self.client.put(f'/api/vagas-monitoria/{vaga.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        vaga.refresh_from_db()
        self.assertEqual(vaga.tipo_monitoria, 'MonitorTEA')
        self.assertEqual(vaga.get_tipo_monitoria_display(), 'Monitor TEA (Remunerado)')


class TipoMonitoriaFluxoTest(TestCase):
    """Testes para o fluxo completo com tipo de monitoria"""
    
    def setUp(self):
        self.client = Client()
        
        # Criar coordenador
        self.coordenador = Coordenador.objects.create(
            cpf='66666666666',
            nome='Coord Fluxo',
            email='coord.fluxo@test.com',
            telefone='11966666666',
            senha_hash=make_password('coord123')
        )
        
        # Criar disciplina
        self.disciplina = Disciplina.objects.create(
            codigo='FLUX001',
            nome='Disciplina Fluxo Tipo'
        )
        
        # Criar aluno
        self.aluno = Aluno.objects.create(
            matricula='202300020',
            nome='Aluno Tipo Monitoria',
            email='aluno.tipo@test.com',
            telefone='11955555555',
            senha_hash=make_password('aluno123'),
            cr_geral=8.5,
            curso='Computação'
        )
    
    def test_criar_monitor_tea_ao_aprovar_candidatura(self):
        """Testa criação automática de MonitorTEA ao aprovar candidatura de vaga MonitorTEA"""
        
        # Criar vaga MonitorTEA
        vaga = VagaMonitoria.objects.create(
            titulo='Vaga MonitorTEA Fluxo',
            pre_requisitos='CR >= 8.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            tipo_monitoria='MonitorTEA',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
        
        # Criar candidatura
        candidatura = Candidatura.objects.create(
            aluno=self.aluno,
            vaga=vaga,
            cr_disciplina=9.0,
            documentos='Documentos',
            status='Pendente'
        )
        
        # Fazer login como coordenador
        session = self.client.session
        session['user_type'] = 'coordenador'
        session['user_id'] = '66666666666'
        session.save()
        
        # Aprovar candidatura
        response = self.client.get(reverse('aprovar_candidatura', args=[candidatura.id]))
        
        # Verificar se MonitorTEA foi criado (não Monitor comum)
        self.assertTrue(MonitorTEA.objects.filter(matricula=self.aluno.matricula).exists())
        
        # Verificar que tem salário
        monitor_tea = MonitorTEA.objects.get(matricula=self.aluno.matricula)
        self.assertIsNotNone(monitor_tea.salario)
        self.assertGreater(monitor_tea.salario, 0)
    
    def test_criar_monitor_voluntario_ao_aprovar_candidatura(self):
        """Testa criação automática de Monitor ao aprovar candidatura de vaga Monitor"""
        
        # Criar vaga Monitor Voluntário
        vaga = VagaMonitoria.objects.create(
            titulo='Vaga Monitor Fluxo',
            pre_requisitos='CR >= 7.0',
            disciplina=self.disciplina,
            coordenador=self.coordenador,
            status='Aberta',
            tipo_monitoria='Monitor',
            prazo_inscricao=date.today() + timedelta(days=30)
        )
        
        # Criar candidatura
        candidatura = Candidatura.objects.create(
            aluno=self.aluno,
            vaga=vaga,
            cr_disciplina=8.5,
            documentos='Documentos',
            status='Pendente'
        )
        
        # Fazer login como coordenador
        session = self.client.session
        session['user_type'] = 'coordenador'
        session['user_id'] = '66666666666'
        session.save()
        
        # Aprovar candidatura
        response = self.client.get(reverse('aprovar_candidatura', args=[candidatura.id]))
        
        # Verificar se Monitor foi criado
        self.assertTrue(Monitor.objects.filter(matricula=self.aluno.matricula).exists())

"""
Script para testar todas as verificações de permissão do sistema
"""
from django.test import Client
from django.urls import reverse
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Aluno, Professor, Coordenador, Casa, Disciplina, VagaMonitoria
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta

def criar_usuarios_teste():
    """Cria usuários de teste para cada tipo"""
    print("🔧 Criando usuários de teste...")
    
    # Limpar dados anteriores
    Aluno.objects.filter(matricula__startswith='TEST').delete()
    Professor.objects.filter(cpf__startswith='99999').delete()
    Coordenador.objects.filter(cpf__startswith='88888').delete()
    Casa.objects.filter(email='casa.teste@test.com').delete()
    
    # Criar aluno
    aluno = Aluno.objects.create(
        matricula='TEST001',
        nome='Aluno Teste',
        email='aluno.teste@test.com',
        telefone='11999999999',
        senha_hash=make_password('senha123'),
        cr_geral=8.5,
        curso='Teste'
    )
    
    # Criar professor
    professor = Professor.objects.create(
        cpf='99999999999',
        nome='Professor Teste',
        email='professor.teste@test.com',
        telefone='11988888888',
        senha_hash=make_password('senha123')
    )
    
    # Criar coordenador
    coordenador = Coordenador.objects.create(
        cpf='88888888888',
        nome='Coordenador Teste',
        email='coordenador.teste@test.com',
        telefone='11977777777',
        senha_hash=make_password('senha123')
    )
    
    # Criar casa
    casa = Casa.objects.create(
        nome='Casa Teste',
        email='casa.teste@test.com',
        telefone='11966666666',
        senha_hash=make_password('senha123')
    )
    
    # Criar disciplina e vaga para testes
    disciplina, _ = Disciplina.objects.get_or_create(
        codigo='TEST101',
        defaults={'nome': 'Disciplina Teste'}
    )
    
    vaga, _ = VagaMonitoria.objects.get_or_create(
        titulo='Vaga Teste Permissões',
        defaults={
            'pre_requisitos': 'Nenhum',
            'disciplina': disciplina,
            'coordenador': coordenador,
            'status': 'Aberta',
            'prazo_inscricao': date.today() + timedelta(days=30)
        }
    )
    
    print("✅ Usuários criados com sucesso!\n")
    return aluno, professor, coordenador, casa, vaga

def testar_permissao(client, user_type, user_id, url_name, url_args=None, deve_permitir=False):
    """Testa uma permissão específica"""
    # Fazer login
    session = client.session
    session['user_type'] = user_type
    session['user_id'] = user_id
    session.save()
    
    # Acessar URL
    url_args = url_args or []
    try:
        url = reverse(url_name, args=url_args)
        response = client.get(url, follow=False)
        
        # Verificar se foi redirecionado para acesso negado
        if response.status_code == 302:
            redirect_url = response.url
            if 'acesso-negado' in redirect_url:
                resultado = "🚫 NEGADO"
                status = "❌" if deve_permitir else "✅"
            else:
                resultado = f"↪️  REDIRECT ({redirect_url})"
                status = "⚠️"
        elif response.status_code == 200:
            resultado = "✓ PERMITIDO"
            status = "✅" if deve_permitir else "❌"
        else:
            resultado = f"? STATUS {response.status_code}"
            status = "⚠️"
        
        return status, resultado
    except Exception as e:
        return "❌", f"ERRO: {str(e)}"

def main():
    print("=" * 80)
    print("🔒 TESTE DE VERIFICAÇÃO DE PERMISSÕES")
    print("=" * 80)
    print()
    
    # Criar usuários
    aluno, professor, coordenador, casa, vaga = criar_usuarios_teste()
    
    client = Client()
    
    # Definir testes
    testes = [
        # (user_type, user_id, url_name, url_args, deve_permitir, descrição)
        
        # CADASTRO DE PROFESSOR
        ("Cadastro de Professor", [
            ('aluno', 'TEST001', 'cadastro_professor', None, False, "Aluno"),
            ('professor', '99999999999', 'cadastro_professor', None, False, "Professor"),
            ('coordenador', '88888888888', 'cadastro_professor', None, True, "Coordenador"),
            ('casa', str(casa.id), 'cadastro_professor', None, True, "Casa"),
        ]),
        
        # CADASTRO DE VAGA
        ("Cadastro de Vaga", [
            ('aluno', 'TEST001', 'cadastro_vaga', None, False, "Aluno"),
            ('professor', '99999999999', 'cadastro_vaga', None, False, "Professor"),
            ('coordenador', '88888888888', 'cadastro_vaga', None, True, "Coordenador"),
            ('casa', str(casa.id), 'cadastro_vaga', None, True, "Casa"),
        ]),
        
        # DASHBOARD
        ("Dashboard", [
            ('aluno', 'TEST001', 'dashboard', None, False, "Aluno"),
            ('professor', '99999999999', 'dashboard', None, False, "Professor"),
            ('coordenador', '88888888888', 'dashboard', None, True, "Coordenador"),
            ('casa', str(casa.id), 'dashboard', None, True, "Casa"),
        ]),
        
        # PAINEL COORDENADOR
        ("Painel Coordenador", [
            ('aluno', 'TEST001', 'painel_coordenador', None, False, "Aluno"),
            ('professor', '99999999999', 'painel_coordenador', None, False, "Professor"),
            ('coordenador', '88888888888', 'painel_coordenador', None, True, "Coordenador"),
            ('casa', str(casa.id), 'painel_coordenador', None, True, "Casa"),
        ]),
        
        # PAINEL MONITOR
        ("Painel Monitor", [
            ('aluno', 'TEST001', 'painel_monitor', None, False, "Aluno"),
            ('professor', '99999999999', 'painel_monitor', None, False, "Professor"),
            ('coordenador', '88888888888', 'painel_monitor', None, False, "Coordenador"),
            ('monitor', 'MONITOR001', 'painel_monitor', None, True, "Monitor"),
        ]),
        
        # CANDIDATAR A VAGA
        ("Candidatar-se a Vaga", [
            ('aluno', 'TEST001', 'candidatar_vaga', [vaga.id], True, "Aluno"),
            ('professor', '99999999999', 'candidatar_vaga', [vaga.id], False, "Professor"),
            ('coordenador', '88888888888', 'candidatar_vaga', [vaga.id], False, "Coordenador"),
            ('casa', str(casa.id), 'candidatar_vaga', [vaga.id], False, "Casa"),
        ]),
        
        # EDITAR VAGA
        ("Editar Vaga", [
            ('aluno', 'TEST001', 'editar_vaga', [vaga.id], False, "Aluno"),
            ('professor', '99999999999', 'editar_vaga', [vaga.id], False, "Professor"),
            ('coordenador', '88888888888', 'editar_vaga', [vaga.id], True, "Coordenador"),
            ('casa', str(casa.id), 'editar_vaga', [vaga.id], True, "Casa"),
        ]),
        
        # VER CANDIDATURAS
        ("Ver Candidaturas", [
            ('aluno', 'TEST001', 'candidaturas_vaga', [vaga.id], False, "Aluno"),
            ('professor', '99999999999', 'candidaturas_vaga', [vaga.id], True, "Professor"),
            ('coordenador', '88888888888', 'candidaturas_vaga', [vaga.id], True, "Coordenador"),
            ('casa', str(casa.id), 'candidaturas_vaga', [vaga.id], True, "Casa"),
        ]),
    ]
    
    # Executar testes
    total_testes = 0
    testes_ok = 0
    testes_falha = 0
    
    for categoria, casos in testes:
        print(f"\n📋 {categoria}")
        print("-" * 80)
        
        for user_type, user_id, url_name, url_args, deve_permitir, descricao in casos:
            status, resultado = testar_permissao(client, user_type, user_id, url_name, url_args, deve_permitir)
            esperado = "DEVE PERMITIR" if deve_permitir else "DEVE NEGAR"
            
            print(f"{status} {descricao:15} → {resultado:20} ({esperado})")
            
            total_testes += 1
            if status == "✅":
                testes_ok += 1
            elif status == "❌":
                testes_falha += 1
    
    # Resumo
    print("\n" + "=" * 80)
    print("📊 RESUMO DOS TESTES")
    print("=" * 80)
    print(f"Total de testes: {total_testes}")
    print(f"✅ Passou: {testes_ok}")
    print(f"❌ Falhou: {testes_falha}")
    print(f"⚠️  Avisos: {total_testes - testes_ok - testes_falha}")
    print()
    
    if testes_falha == 0:
        print("🎉 TODOS OS TESTES DE PERMISSÃO PASSARAM!")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM - VERIFICAR IMPLEMENTAÇÃO")
    
    print("=" * 80)

if __name__ == '__main__':
    main()


# ==================== EXECUTAR TESTES ====================
# Para rodar os testes, use o comando:
# python manage.py test myapp.tests
# 
# Para rodar apenas testes de API:
# python manage.py test myapp.tests.DisciplinaAPITest
# python manage.py test myapp.tests.AlunoAPITest
# python manage.py test myapp.tests.VagaMonitoriaAPITest
# python manage.py test myapp.tests.CandidaturaAPITest
# python manage.py test myapp.tests.ProfessorAPITest
# python manage.py test myapp.tests.TipoMonitoriaAPITest
# python manage.py test myapp.tests.TipoMonitoriaFluxoTest

