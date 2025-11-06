from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.models import (
    Aluno, Monitor, MonitorTEA, Professor, Coordenador,
    Disciplina, VagaMonitoria, Candidatura, RegistroMonitoria
)


# Home page
def home(request):
    context = {
        'vagas_abertas': VagaMonitoria.objects.filter(status='Aberta').count(),
        'total_monitores': Monitor.objects.count() + MonitorTEA.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
    }
    
    if request.user.is_authenticated:
        # Adicionar dados específicos do usuário se necessário
        pass
    
    return render(request, 'home.html', context)


# Login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        try:
            # Buscar usuário baseado no tipo
            user = None
            user_id = None
            
            if user_type == 'aluno':
                # Buscar aluno por email
                user = Aluno.objects.filter(email=email).first()
                if user:
                    user_id = user.matricula
            elif user_type == 'professor':
                # Buscar professor por email
                user = Professor.objects.filter(email=email).first()
                if user:
                    user_id = user.cpf
            elif user_type == 'coordenador':
                # Buscar coordenador por email
                user = Coordenador.objects.filter(email=email).first()
                if user:
                    user_id = user.cpf
            elif user_type == 'monitor':
                # Buscar monitor por email
                user = Monitor.objects.filter(email=email).first()
                if user:
                    user_id = user.matricula
            
            # Verificar senha
            if user and check_password(password, user.senha_hash):
                # Login bem-sucedido
                request.session['user_type'] = user_type
                request.session['user_id'] = user_id
                request.session['user_email'] = email
                request.session['user_nome'] = user.nome
                return redirect('home')
            else:
                messages.error(request, 'Email ou senha incorretos.')
        
        except Exception as e:
            messages.error(request, f'Erro ao realizar login: {str(e)}')
    
    return render(request, 'login.html')


# Logout
def logout_view(request):
    # Limpar a sessão
    request.session.flush()
    return redirect('login')


# Cadastro de Aluno
def cadastro_aluno(request):
    if request.method == 'POST':
        try:
            aluno = Aluno(
                matricula=request.POST.get('matricula'),
                nome=request.POST.get('nome'),
                email=request.POST.get('email'),
                telefone=request.POST.get('telefone'),
                senha_hash=make_password(request.POST.get('senha')),
                cr_geral=request.POST.get('cr_geral'),
                curso=request.POST.get('curso')
            )
            aluno.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    return render(request, 'cadastro_aluno.html')


# Cadastro de Professor (apenas Coordenador e Casa)
def cadastro_professor(request):
    # Verificar permissão - apenas coordenador e casa podem cadastrar professores
    user_type = request.session.get('user_type')
    if user_type not in ['coordenador', 'casa']:
        messages.error(request, 'Apenas coordenadores podem cadastrar novos professores.')
        return redirect('home')
    
    if request.method == 'POST':
        try:
            is_coordenador = request.POST.get('is_coordenador') == '1'
            
            # Apenas Casa pode cadastrar Coordenadores
            if is_coordenador and user_type != 'casa':
                messages.error(request, 'Apenas Casa pode cadastrar coordenadores.')
                return redirect('cadastro_professor')
            
            if is_coordenador:
                usuario = Coordenador(
                    cpf=request.POST.get('cpf'),
                    nome=request.POST.get('nome'),
                    email=request.POST.get('email'),
                    telefone=request.POST.get('telefone'),
                    senha_hash=make_password(request.POST.get('senha'))
                )
            else:
                usuario = Professor(
                    cpf=request.POST.get('cpf'),
                    nome=request.POST.get('nome'),
                    email=request.POST.get('email'),
                    telefone=request.POST.get('telefone'),
                    senha_hash=make_password(request.POST.get('senha'))
                )
            
            usuario.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('painel_coordenador')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    return render(request, 'cadastro_professor.html')


# Lista de Vagas
def lista_vagas(request):
    vagas = VagaMonitoria.objects.all().select_related('disciplina', 'coordenador')
    context = {'vagas': vagas}
    return render(request, 'lista_vagas.html', context)


# Cadastro de Vaga (apenas coordenadores)
def cadastro_vaga(request):
    # Verificar permissão
    user_type = request.session.get('user_type')
    if user_type not in ['coordenador', 'casa']:
        messages.error(request, 'Apenas coordenadores podem cadastrar vagas.')
        return redirect('lista_vagas')
    
    if request.method == 'POST':
        try:
            # Buscar coordenador logado
            coordenador = None
            if user_type == 'coordenador':
                user_cpf = request.session.get('user_id')
                coordenador = Coordenador.objects.filter(cpf=user_cpf).first()
            elif user_type == 'casa':
                # Casa também pode criar vagas, mas usa seu CPF como coordenador
                from myapp.models import Casa
                user_cpf = request.session.get('user_id')
                casa = Casa.objects.filter(cpf=user_cpf).first()
                # Casa herda de Coordenador, então podemos usar diretamente
                if casa:
                    coordenador = Coordenador.objects.filter(cpf=user_cpf).first()
            
            vaga = VagaMonitoria(
                titulo=request.POST.get('titulo'),
                pre_requisitos=request.POST.get('pre_requisitos'),
                disciplina_id=request.POST.get('disciplina'),
                prazo_inscricao=request.POST.get('prazo_inscricao'),
                status=request.POST.get('status', 'Aberta'),
                coordenador=coordenador
            )
            vaga.save()
            messages.success(request, 'Vaga cadastrada com sucesso!')
            return redirect('lista_vagas')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar vaga: {str(e)}')
    
    disciplinas = Disciplina.objects.all()
    context = {'disciplinas': disciplinas}
    return render(request, 'cadastro_vaga.html', context)


# Painel do Monitor
# @login_required  # Temporariamente desabilitado para testes
def painel_monitor(request):
    # Assumindo que request.user é um Monitor ou MonitorTEA
    context = {
        'atividades_pendentes': [],
        'historico': [],
    }
    return render(request, 'painel_monitor.html', context)


# Painel do Coordenador
# @login_required  # Temporariamente desabilitado para testes
def painel_coordenador(request):
    context = {
        'candidaturas_pendentes': Candidatura.objects.filter(status='Pendente').select_related('aluno', 'vaga'),
        'minhas_vagas': VagaMonitoria.objects.all(),
        'monitores_ativos': list(Monitor.objects.all()) + list(MonitorTEA.objects.all()),
        'registros_pendentes': RegistroMonitoria.objects.all()[:10],
    }
    return render(request, 'painel_coordenador.html', context)


# Dashboard de Métricas
# @login_required  # Temporariamente desabilitado para testes
def dashboard(request):
    total_vagas = VagaMonitoria.objects.count()
    vagas_abertas = VagaMonitoria.objects.filter(status='Aberta').count()
    vagas_fechadas = VagaMonitoria.objects.filter(status='Fechada').count()
    vagas_analise = VagaMonitoria.objects.filter(status='Em Análise').count()
    
    context = {
        'total_vagas': total_vagas,
        'total_candidaturas': Candidatura.objects.count(),
        'monitores_ativos': Monitor.objects.count() + MonitorTEA.objects.count(),
        'horas_monitoria': 0,  # Calcular soma de horas
        'taxa_aprovacao': 75,  # Calcular taxa real
        'alunos_atendidos': 0,  # Calcular total de alunos únicos
        'vagas_abertas': vagas_abertas,
        'vagas_fechadas': vagas_fechadas,
        'vagas_analise': vagas_analise,
        'vagas_abertas_percent': round((vagas_abertas / total_vagas * 100) if total_vagas > 0 else 0, 1),
        'vagas_fechadas_percent': round((vagas_fechadas / total_vagas * 100) if total_vagas > 0 else 0, 1),
        'vagas_analise_percent': round((vagas_analise / total_vagas * 100) if total_vagas > 0 else 0, 1),
        'novas_vagas_mes': 0,
        'candidaturas_mes': 0,
        'monitores_novos': 0,
        'horas_mes': 0,
        'alunos_mes': 0,
        'top_monitores': [],
    }
    return render(request, 'dashboard.html', context)


# Registrar Monitoria
# @login_required  # Temporariamente desabilitado para testes
def registrar_monitoria(request):
    if request.method == 'POST':
        try:
            # Calcular horas trabalhadas
            from datetime import datetime
            inicio = datetime.strptime(request.POST.get('horario_inicio'), '%H:%M')
            fim = datetime.strptime(request.POST.get('horario_fim'), '%H:%M')
            horas = (fim - inicio).seconds / 3600
            
            registro = RegistroMonitoria(
                # monitor_tea=request.user,  # Assumindo usuário logado
                data_monitoria=request.POST.get('data_monitoria'),
                horario_inicio=request.POST.get('horario_inicio'),
                horario_fim=request.POST.get('horario_fim'),
                horas_trabalhadas=horas,
                codigo_disciplina=request.POST.get('codigo_disciplina'),
                descricao_atividade=request.POST.get('descricao_atividade'),
                quantidade_alunos=request.POST.get('quantidade_alunos'),
                observacoes=request.POST.get('observacoes', ''),
            )
            # registro.save()
            messages.success(request, 'Monitoria registrada com sucesso!')
            return redirect('painel_monitor')
        except Exception as e:
            messages.error(request, f'Erro ao registrar monitoria: {str(e)}')
    
    return redirect('painel_monitor')


# Presença dos Alunos
# @login_required  # Temporariamente desabilitado para testes
def presenca_alunos(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            matricula = request.POST.get('matricula')
            
            # In production, save presence to database
            # Presenca.objects.create(aluno_nome=nome, aluno_matricula=matricula)
            
            messages.success(request, f'Presença registrada para {nome}!')
            return redirect('presenca_alunos')
        except Exception as e:
            messages.error(request, f'Erro ao registrar presença: {str(e)}')
    
    context = {
        'presencas': [],  # In production, fetch from database
        'total_presencas': 12,
        'presencas_24h': 8,
    }
    
    return render(request, 'presenca_alunos.html', context)


# Detalhes da Vaga
def detalhes_vaga(request, vaga_id):
    vaga = get_object_or_404(VagaMonitoria, id=vaga_id)
    context = {'vaga': vaga}
    return render(request, 'detalhes_vaga.html', context)


# Candidatar-se a uma vaga
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(VagaMonitoria, id=vaga_id)
    
    # Verificar se o usuário é aluno
    if request.session.get('user_type') != 'aluno':
        messages.error(request, 'Apenas alunos podem se candidatar a vagas.')
        return redirect('lista_vagas')
    
    if request.method == 'POST':
        try:
            # Obter matrícula do aluno logado da sessão
            matricula_aluno = request.session.get('user_id')
            if not matricula_aluno:
                messages.error(request, 'Você precisa estar logado como aluno para se candidatar.')
                return redirect('login')
            
            # Buscar o aluno no banco
            aluno = get_object_or_404(Aluno, matricula=matricula_aluno)
            
            # Verificar se já existe candidatura
            candidatura_existente = Candidatura.objects.filter(aluno=aluno, vaga=vaga).first()
            if candidatura_existente:
                messages.warning(request, 'Você já se candidatou a esta vaga.')
                return redirect('lista_vagas')
            
            # Criar nova candidatura
            candidatura = Candidatura(
                aluno=aluno,
                vaga=vaga,
                cr_disciplina=float(request.POST.get('cr_disciplina')),
                documentos=request.POST.get('documentos', ''),
                status='Pendente'
            )
            candidatura.save()
            
            messages.success(request, 'Candidatura enviada com sucesso!')
            return redirect('lista_vagas')
        except Exception as e:
            messages.error(request, f'Erro ao enviar candidatura: {str(e)}')
    
    context = {'vaga': vaga}
    return render(request, 'candidatar_vaga.html', context)


# Editar Vaga
def editar_vaga(request, vaga_id):
    # Verificar permissão
    user_type = request.session.get('user_type')
    if user_type not in ['coordenador', 'casa']:
        messages.error(request, 'Você não tem permissão para editar vagas.')
        return redirect('lista_vagas')
    
    vaga = get_object_or_404(VagaMonitoria, id=vaga_id)
    
    if request.method == 'POST':
        try:
            vaga.titulo = request.POST.get('titulo')
            vaga.pre_requisitos = request.POST.get('pre_requisitos')
            vaga.disciplina_id = request.POST.get('disciplina')
            vaga.prazo_inscricao = request.POST.get('prazo_inscricao')
            vaga.status = request.POST.get('status')
            vaga.save()
            messages.success(request, 'Vaga atualizada com sucesso!')
            return redirect('lista_vagas')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar vaga: {str(e)}')
    
    disciplinas = Disciplina.objects.all()
    context = {
        'vaga': vaga,
        'disciplinas': disciplinas
    }
    return render(request, 'editar_vaga.html', context)


# Ver Candidaturas de uma Vaga
def candidaturas_vaga(request, vaga_id):
    # Verificar permissão
    user_type = request.session.get('user_type')
    if user_type not in ['coordenador', 'casa']:
        messages.error(request, 'Você não tem permissão para visualizar candidaturas.')
        return redirect('lista_vagas')
    
    vaga = get_object_or_404(VagaMonitoria, id=vaga_id)
    candidaturas = Candidatura.objects.filter(vaga=vaga).select_related('aluno').order_by('-data_candidatura')
    
    context = {
        'vaga': vaga,
        'candidaturas': candidaturas
    }
    return render(request, 'candidaturas_vaga.html', context)


# Detalhes da Candidatura
# @login_required  # Temporariamente desabilitado para testes
def detalhes_candidatura(request, candidatura_id):
    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    
    context = {
        'candidatura': candidatura,
        'cr_valido': candidatura.validarCR()
    }
    return render(request, 'detalhes_candidatura.html', context)


# Aprovar Candidatura
def aprovar_candidatura(request, candidatura_id):
    # Verificar permissão
    user_type = request.session.get('user_type')
    if user_type not in ['coordenador', 'casa']:
        messages.error(request, 'Você não tem permissão para aprovar candidaturas.')
        return redirect('lista_vagas')
    
    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    
    try:
        candidatura.status = 'Aprovada'
        candidatura.save()
        
        # Criar registro de Monitor se ainda não existir
        Monitor.objects.get_or_create(
            matricula=candidatura.aluno.matricula,
            defaults={
                'nome': candidatura.aluno.nome,
                'email': candidatura.aluno.email,
                'telefone': candidatura.aluno.telefone,
                'senha_hash': candidatura.aluno.senha_hash,
                'cr_geral': candidatura.aluno.cr_geral,
                'curso': candidatura.aluno.curso
            }
        )
        
        messages.success(request, f'Candidatura de {candidatura.aluno.nome} aprovada com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao aprovar candidatura: {str(e)}')
    
    return redirect('candidaturas_vaga', vaga_id=candidatura.vaga.id)


# Rejeitar Candidatura
def rejeitar_candidatura(request, candidatura_id):
    # Verificar permissão
    user_type = request.session.get('user_type')
    if user_type not in ['coordenador', 'casa']:
        messages.error(request, 'Você não tem permissão para rejeitar candidaturas.')
        return redirect('lista_vagas')
    
    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    
    try:
        candidatura.status = 'Rejeitada'
        candidatura.save()
        messages.success(request, f'Candidatura de {candidatura.aluno.nome} rejeitada.')
    except Exception as e:
        messages.error(request, f'Erro ao rejeitar candidatura: {str(e)}')
    
    return redirect('candidaturas_vaga', vaga_id=candidatura.vaga.id)


# Detalhes do Monitor
# @login_required  # Temporariamente desabilitado para testes
def detalhes_monitor(request, matricula):
    monitor = get_object_or_404(Monitor, matricula=matricula)
    
    # Buscar candidaturas aprovadas do monitor
    candidaturas_aprovadas = Candidatura.objects.filter(
        aluno__matricula=matricula,
        status='Aprovada'
    ).select_related('vaga', 'vaga__disciplina')
    
    # Se for MonitorTEA, buscar registros de monitoria
    registros = []
    is_monitor_tea = False
    try:
        monitor_tea = MonitorTEA.objects.get(matricula=matricula)
        is_monitor_tea = True
        registros = RegistroMonitoria.objects.filter(
            monitor_tea=monitor_tea
        ).order_by('-data_monitoria')[:10]
    except MonitorTEA.DoesNotExist:
        pass
    
    context = {
        'monitor': monitor,
        'is_monitor_tea': is_monitor_tea,
        'candidaturas_aprovadas': candidaturas_aprovadas,
        'registros': registros
    }
    return render(request, 'detalhes_monitor.html', context)
