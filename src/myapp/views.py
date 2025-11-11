from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from myapp.models import (
    Aluno, Monitor, MonitorTEA, Professor, Coordenador,
    Disciplina, VagaMonitoria, Candidatura, RegistroMonitoria, Casa
)


def home(request):
    context = {
        'vagas_abertas': VagaMonitoria.objects.filter(status='Aberta').count(),
        'total_monitores': Monitor.objects.count() + MonitorTEA.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
    }
    
    if request.user.is_authenticated:
        pass
    
    return render(request, 'home.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        try:
            user = None
            user_id = None
            
            if user_type == 'aluno':
                user = Aluno.objects.filter(email=email).first()
                if user:
                    user_id = user.matricula
            elif user_type == 'professor':
                user = Professor.objects.filter(email=email).first()
                if user:
                    user_id = user.cpf
            elif user_type == 'casa':
                user = Casa.objects.filter(email=email).first()
                if user:
                    user_id = user.email
            elif user_type == 'coordenador':
                user = Coordenador.objects.filter(email=email).first()
                if user:
                    user_id = user.cpf
            elif user_type == 'monitor':
                user = Monitor.objects.filter(email=email).first()
                if user:
                    user_id = user.matricula
            
            if user and check_password(password, user.senha_hash):
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


def logout_view(request):
    request.session.flush()
    return redirect('login')


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


def lista_vagas(request):
    vagas = VagaMonitoria.objects.all().select_related('disciplina', 'coordenador')
    context = {'vagas': vagas}
    return render(request, 'lista_vagas.html', context)


def cadastro_vaga(request):
    user_type = request.session.get('user_type')
    if user_type != 'coordenador':
        messages.error(request, 'Apenas coordenadores podem cadastrar vagas.')
        return redirect('lista_vagas')
    
    if request.method == 'POST':
        try:
            user_cpf = request.session.get('user_id')
            coordenador = get_object_or_404(Coordenador, cpf=user_cpf)
            
            vaga = VagaMonitoria(
                titulo=request.POST.get('titulo'),
                pre_requisitos=request.POST.get('pre_requisitos'),
                disciplina_id=request.POST.get('disciplina'),
                prazo_inscricao=request.POST.get('prazo_inscricao'),
                status=request.POST.get('status', 'Aberta'),
                tipo_monitoria=request.POST.get('tipo_monitoria', 'Monitor'),
                coordenador=coordenador
            )
            coordenador.cadastrarVaga(vaga)
            
            messages.success(request, 'Vaga cadastrada com sucesso!')
            return redirect('lista_vagas')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar vaga: {str(e)}')
    
    disciplinas = Disciplina.objects.all()
    context = {'disciplinas': disciplinas}
    return render(request, 'cadastro_vaga.html', context)


def painel_monitor(request):
    context = {
        'atividades_pendentes': [],
        'historico': [],
    }
    return render(request, 'painel_monitor.html', context)


def painel_coordenador(request):
    user_type = request.session.get('user_type')
    
    context = {
        'candidaturas_pendentes': Candidatura.objects.filter(status='Pendente').select_related('aluno', 'vaga'),
        'minhas_vagas': VagaMonitoria.objects.all(),
        'monitores_ativos': list(Monitor.objects.all()) + list(MonitorTEA.objects.all()),
        'registros_pendentes': RegistroMonitoria.objects.all()[:10],
        'user_type': user_type
    }
    return render(request, 'painel_coordenador.html', context)


def dashboard(request):
    user_type = request.session.get('user_type')
    if user_type not in ['coordenador', 'casa']:
        messages.error(request, 'Acesso negado. Apenas coordenadores e administradores podem acessar o dashboard.')
        return redirect('home')
    
    # Métricas principais
    total_vagas = VagaMonitoria.objects.count()
    vagas_abertas = VagaMonitoria.objects.filter(status='Aberta').count()
    vagas_fechadas = VagaMonitoria.objects.filter(status='Fechada').count()
    vagas_analise = VagaMonitoria.objects.filter(status='Em Análise').count()
    
    total_candidaturas = Candidatura.objects.count()
    candidaturas_aprovadas = Candidatura.objects.filter(status='Aprovada').count()
    candidaturas_pendentes = Candidatura.objects.filter(status='Pendente').count()
    
    taxa_aprovacao = round((candidaturas_aprovadas / total_candidaturas * 100) if total_candidaturas > 0 else 0, 1)
    
    total_monitores = Monitor.objects.count()
    total_monitores_tea = MonitorTEA.objects.count()
    monitores_ativos = total_monitores + total_monitores_tea
    
    from django.db.models import Sum
    horas_totais = RegistroMonitoria.objects.aggregate(
        total=Sum('horas_trabalhadas')
    )['total'] or 0
    
    alunos_participantes_list = []
    for registro in RegistroMonitoria.objects.all():
        for aluno in registro.alunos_participantes:
            matricula = aluno.get('matricula')
            if matricula and matricula not in alunos_participantes_list:
                alunos_participantes_list.append(matricula)
    alunos_atendidos = len(alunos_participantes_list)
    
    # ========== MÉTRICAS DO MÊS ATUAL ==========
    
    from django.utils import timezone
    primeiro_dia_mes = date.today().replace(day=1)
    
    # Novas vagas este mês
    novas_vagas_mes = VagaMonitoria.objects.filter(
        prazo_inscricao__gte=primeiro_dia_mes
    ).count()
    
    # Candidaturas este mês
    candidaturas_mes = Candidatura.objects.filter(
        data_candidatura__gte=primeiro_dia_mes
    ).count()
    
    # Monitores novos este mês (baseado em candidaturas aprovadas)
    monitores_novos = Candidatura.objects.filter(
        status='Aprovada',
        data_candidatura__gte=primeiro_dia_mes
    ).count()
    
    # Horas de monitoria este mês
    horas_mes = RegistroMonitoria.objects.filter(
        data_monitoria__gte=primeiro_dia_mes
    ).aggregate(total=Sum('horas_trabalhadas'))['total'] or 0
    
    # Alunos atendidos este mês
    alunos_mes_list = []
    for registro in RegistroMonitoria.objects.filter(data_monitoria__gte=primeiro_dia_mes):
        for aluno in registro.alunos_participantes:
            matricula = aluno.get('matricula')
            if matricula and matricula not in alunos_mes_list:
                alunos_mes_list.append(matricula)
    alunos_mes = len(alunos_mes_list)
    
    # ========== DADOS PARA GRÁFICOS ==========
    
    # Gráfico de Presença por Dia (últimos 7 dias)
    presenca_por_dia = []
    labels_dias = []
    for i in range(6, -1, -1):
        dia = date.today() - timedelta(days=i)
        registros_dia = RegistroMonitoria.objects.filter(data_monitoria=dia)
        total_alunos_dia = sum(r.quantidade_alunos for r in registros_dia)
        presenca_por_dia.append(total_alunos_dia)
        labels_dias.append(dia.strftime('%d/%m'))
    
    # Gráfico de Distribuição por Disciplina
    from django.db.models import Count
    disciplinas_count = VagaMonitoria.objects.values('disciplina__nome').annotate(
        total=Count('id')
    ).order_by('-total')[:6]
    
    disciplinas_labels = [d['disciplina__nome'] for d in disciplinas_count]
    disciplinas_valores = [d['total'] for d in disciplinas_count]
    
    # ========== LISTA DE MONITORIAS RECENTES ==========
    
    monitorias_recentes = []
    registros_recentes = RegistroMonitoria.objects.select_related(
        'monitor_tea', 'candidatura__vaga__disciplina'
    ).order_by('-data_monitoria', '-horario_inicio')[:20]
    
    for registro in registros_recentes:
        try:
            disciplina = registro.candidatura.vaga.disciplina.nome if registro.candidatura and registro.candidatura.vaga else registro.codigo_disciplina
        except:
            disciplina = registro.codigo_disciplina
            
        monitorias_recentes.append({
            'id': registro.id,
            'monitor': registro.monitor_tea.nome,
            'disciplina': disciplina,
            'codigo_disciplina': registro.codigo_disciplina,
            'data': registro.data_monitoria,
            'horario_inicio': registro.horario_inicio,
            'horario_fim': registro.horario_fim,
            'horas_trabalhadas': float(registro.horas_trabalhadas),
            'quantidade_alunos': registro.quantidade_alunos,
            'alunos_participantes': registro.alunos_participantes,
            'descricao': registro.descricao_atividade[:100] + '...' if len(registro.descricao_atividade) > 100 else registro.descricao_atividade,
        })
    
    # == ATIVIDADES RECENTES (FEED) ==
    
    atividades_recentes = []
    
    # Candidaturas recentes
    for candidatura in Candidatura.objects.order_by('-data_candidatura')[:3]:
        tempo = calcular_tempo_decorrido(candidatura.data_candidatura)
        atividades_recentes.append({
            'tipo': 'candidatura',
            'descricao': f"Nova candidatura para {candidatura.vaga.disciplina.nome}",
            'tempo': tempo,
            'data': candidatura.data_candidatura
        })
    
    # Monitorias recentes
    for registro in RegistroMonitoria.objects.order_by('-data_monitoria')[:3]:
        tempo = calcular_tempo_decorrido(registro.data_monitoria)
        atividades_recentes.append({
            'tipo': 'monitoria',
            'descricao': f"Monitoria registrada - {float(registro.horas_trabalhadas)}h - {registro.quantidade_alunos} alunos",
            'tempo': tempo,
            'data': registro.data_monitoria
        })
    
    # Vagas recentes
    for vaga in VagaMonitoria.objects.order_by('-id')[:2]:
        tempo = calcular_tempo_decorrido(vaga.prazo_inscricao)
        atividades_recentes.append({
            'tipo': 'vaga',
            'descricao': f"Nova vaga cadastrada - {vaga.disciplina.nome}",
            'tempo': tempo,
            'data': vaga.prazo_inscricao
        })
    
    # Ordenar por data (mais recente primeiro)
    atividades_recentes.sort(key=lambda x: x['data'], reverse=True)
    atividades_recentes = atividades_recentes[:8]  # Limitar a 8 itens
    
    # ========== ESTATÍSTICAS POR TIPO DE MONITORIA ==========
    
    vagas_monitor = VagaMonitoria.objects.filter(tipo_monitoria='Monitor').count()
    vagas_monitor_tea = VagaMonitoria.objects.filter(tipo_monitoria='MonitorTEA').count()
    
    # Converter listas para JSON para uso nos gráficos
    import json
    presenca_labels_json = json.dumps(labels_dias)
    presenca_data_json = json.dumps(presenca_por_dia)
    disciplinas_labels_json = json.dumps(disciplinas_labels)
    disciplinas_data_json = json.dumps(disciplinas_valores)
    
    context = {
        # Métricas principais
        'total_vagas': total_vagas,
        'total_candidaturas': total_candidaturas,
        'monitores_ativos': monitores_ativos,
        'horas_monitoria': round(float(horas_totais), 1),
        'taxa_aprovacao': taxa_aprovacao,
        'alunos_atendidos': alunos_atendidos,
        
        # Status das vagas
        'vagas_abertas': vagas_abertas,
        'vagas_fechadas': vagas_fechadas,
        'vagas_analise': vagas_analise,
        'vagas_abertas_percent': round((vagas_abertas / total_vagas * 100) if total_vagas > 0 else 0, 1),
        'vagas_fechadas_percent': round((vagas_fechadas / total_vagas * 100) if total_vagas > 0 else 0, 1),
        'vagas_analise_percent': round((vagas_analise / total_vagas * 100) if total_vagas > 0 else 0, 1),
        
        # Métricas do mês
        'novas_vagas_mes': novas_vagas_mes,
        'candidaturas_mes': candidaturas_mes,
        'monitores_novos': monitores_novos,
        'horas_mes': round(float(horas_mes), 1),
        'alunos_mes': alunos_mes,
        
        # Dados para gráficos (formato JSON)
        'presenca_labels': presenca_labels_json,
        'presenca_data': presenca_data_json,
        'disciplinas_labels': disciplinas_labels_json,
        'disciplinas_data': disciplinas_data_json,
        
        # Listas
        'monitorias_recentes': monitorias_recentes,
        'atividades_recentes': atividades_recentes,
        
        # Estatísticas adicionais
        'total_monitores': total_monitores,
        'total_monitores_tea': total_monitores_tea,
        'vagas_monitor': vagas_monitor,
        'vagas_monitor_tea': vagas_monitor_tea,
        'candidaturas_aprovadas': candidaturas_aprovadas,
        'candidaturas_pendentes': candidaturas_pendentes,
    }
    
    return render(request, 'dashboard.html', context)


def calcular_tempo_decorrido(data_passada):
    """Calcula quanto tempo se passou desde uma data"""
    if isinstance(data_passada, datetime):
        data_passada = data_passada.date()
    
    hoje = date.today()
    diferenca = (hoje - data_passada).days
    
    if diferenca == 0:
        return "Hoje"
    elif diferenca == 1:
        return "Ontem"
    elif diferenca < 7:
        return f"{diferenca} dias atrás"
    elif diferenca < 30:
        semanas = diferenca // 7
        return f"{semanas} semana{'s' if semanas > 1 else ''} atrás"
    else:
        meses = diferenca // 30
        return f"{meses} mês{'es' if meses > 1 else ''} atrás"
    return render(request, 'dashboard.html', context)


# Registrar Monitoria
# @login_required  # Temporariamente desabilitado para testes
def registrar_monitoria(request):
    if request.method == 'POST':
        try:
            # Calcular horas trabalhadas
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
    """View para monitor registrar presença de alunos na monitoria"""
    
    # Verificar se o usuário é monitor
    user_type = request.session.get('user_type')
    if user_type != 'monitor':
        messages.error(request, 'Apenas monitores podem registrar presença de alunos.')
        return redirect('home')
    
    # Buscar o monitor logado
    user_id = request.session.get('user_id')
    
    # Tentar buscar como Monitor ou MonitorTEA
    try:
        monitor = Monitor.objects.get(matricula=user_id)
        is_monitor_tea = False
    except Monitor.DoesNotExist:
        try:
            monitor = MonitorTEA.objects.get(matricula=user_id)
            is_monitor_tea = True
        except MonitorTEA.DoesNotExist:
            messages.error(request, 'Monitor não encontrado.')
            return redirect('home')
    
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            matricula = request.POST.get('matricula')
            
            # Validar dados
            if not nome or not matricula:
                messages.error(request, 'Nome e matrícula são obrigatórios.')
                return redirect('presenca_alunos')
            
            # Verificar se o aluno existe
            try:
                aluno = Aluno.objects.get(matricula=matricula)
                # Atualizar nome se necessário
                if aluno.nome != nome:
                    messages.warning(request, f'Nome informado difere do cadastro. Aluno: {aluno.nome}')
            except Aluno.DoesNotExist:
                messages.warning(request, f'Aluno com matrícula {matricula} não encontrado no sistema.')
            
            # Registrar presença (vamos criar um modelo simples de Presenca depois)
            # Por enquanto, vamos adicionar ao campo alunos_participantes de um RegistroMonitoria
            
            # Buscar ou criar registro de monitoria do dia atual
            hoje = date.today()
            
            # Buscar candidatura aprovada do monitor (última)
            candidaturas = Candidatura.objects.filter(
                aluno__matricula=user_id,
                status='Aprovada'
            ).order_by('-id')
            
            if not candidaturas.exists():
                messages.error(request, 'Nenhuma candidatura aprovada encontrada.')
                return redirect('presenca_alunos')
            
            candidatura = candidaturas.first()
            
            # Buscar ou criar registro de monitoria do dia
            if is_monitor_tea:
                registro, created = RegistroMonitoria.objects.get_or_create(
                    monitor_tea=monitor,
                    data_monitoria=hoje,
                    candidatura=candidatura,
                    defaults={
                        'horario_inicio': datetime.now().time(),
                        'horario_fim': datetime.now().time(),
                        'horas_trabalhadas': 0,
                        'codigo_disciplina': candidatura.vaga.disciplina.codigo,
                        'descricao_atividade': 'Monitoria do dia',
                        'alunos_participantes': [],
                        'quantidade_alunos': 0
                    }
                )
                
                # Adicionar aluno à lista de participantes
                if not any(p.get('matricula') == matricula for p in registro.alunos_participantes):
                    registro.alunos_participantes.append({
                        'matricula': matricula,
                        'nome': nome
                    })
                    registro.quantidade_alunos = len(registro.alunos_participantes)
                    registro.save()
                    
                    messages.success(request, f'Presença registrada para {nome} (Matrícula: {matricula})!')
                else:
                    messages.warning(request, f'{nome} já tem presença registrada hoje.')
            else:
                # Para Monitor voluntário, apenas mostrar mensagem (não há RegistroMonitoria obrigatório)
                messages.success(request, f'Presença registrada para {nome} (Matrícula: {matricula})!')
            
            return redirect('presenca_alunos')
            
        except Exception as e:
            messages.error(request, f'Erro ao registrar presença: {str(e)}')
    
    # Listar presenças registradas
    presencas_list = []
    total_presencas = 0
    presencas_24h = 0
    
    try:
        if is_monitor_tea:
            # Buscar registros do monitor TEA
            registros = RegistroMonitoria.objects.filter(
                monitor_tea=monitor
            ).order_by('-data_monitoria')[:10]
            
            for registro in registros:
                for aluno in registro.alunos_participantes:
                    presencas_list.append({
                        'id': f"{registro.id}_{aluno.get('matricula')}",
                        'aluno_nome': aluno.get('nome', ''),
                        'aluno_matricula': aluno.get('matricula', ''),
                        'data': registro.data_monitoria,
                        'hora': registro.horario_inicio
                    })
            
            # Contar totais
            total_registros = RegistroMonitoria.objects.filter(monitor_tea=monitor)
            total_presencas = sum(r.quantidade_alunos for r in total_registros)
            
            # Últimas 24h
            from datetime import timedelta
            ontem = date.today() - timedelta(days=1)
            registros_24h = RegistroMonitoria.objects.filter(
                monitor_tea=monitor,
                data_monitoria__gte=ontem
            )
            presencas_24h = sum(r.quantidade_alunos for r in registros_24h)
    except Exception as e:
        messages.error(request, f'Erro ao buscar presenças: {str(e)}')
    
    context = {
        'presencas': presencas_list,
        'total_presencas': total_presencas,
        'presencas_24h': presencas_24h,
        'is_monitor_tea': is_monitor_tea
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
    # Verificar permissão - APENAS COORDENADOR
    user_type = request.session.get('user_type')
    if user_type != 'coordenador':
        messages.error(request, 'Apenas coordenadores podem editar vagas.')
        return redirect('lista_vagas')
    
    vaga = get_object_or_404(VagaMonitoria, id=vaga_id)
    
    # Verificar se o coordenador logado é o dono da vaga
    user_cpf = request.session.get('user_id')
    coordenador = get_object_or_404(Coordenador, cpf=user_cpf)
    
    if vaga.coordenador and vaga.coordenador.cpf != coordenador.cpf:
        messages.error(request, 'Você só pode editar suas próprias vagas.')
        return redirect('lista_vagas')
    
    if request.method == 'POST':
        try:
            vaga.titulo = request.POST.get('titulo')
            vaga.pre_requisitos = request.POST.get('pre_requisitos')
            vaga.disciplina_id = request.POST.get('disciplina')
            vaga.prazo_inscricao = request.POST.get('prazo_inscricao')
            vaga.status = request.POST.get('status')
            vaga.tipo_monitoria = request.POST.get('tipo_monitoria')
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
    # Verificar permissão - Professores, coordenadores e casa podem ver
    user_type = request.session.get('user_type')
    if user_type not in ['coordenador', 'professor', 'casa']:
        messages.error(request, 'Você não tem permissão para visualizar candidaturas.')
        return redirect('lista_vagas')
    
    vaga = get_object_or_404(VagaMonitoria, id=vaga_id)
    candidaturas = Candidatura.objects.filter(vaga=vaga).select_related('aluno').order_by('-data_candidatura')
    
    context = {
        'vaga': vaga,
        'candidaturas': candidaturas,
        'user_type': user_type
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
    # Verificar permissão - Apenas professores, coordenadores e casa
    user_type = request.session.get('user_type')
    if user_type not in ['professor', 'coordenador', 'casa']:
        messages.error(request, 'Apenas professores podem aprovar candidaturas.')
        return redirect('lista_vagas')
    
    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    
    try:
        # Verificar o tipo de monitoria da vaga
        tipo_monitoria = candidatura.vaga.tipo_monitoria
        
        # Buscar o professor logado
        if user_type in ['professor', 'coordenador']:
            user_cpf = request.session.get('user_id')
            professor = get_object_or_404(Professor, cpf=user_cpf)
            
            # Aprovar candidatura
            candidatura.status = 'Aprovada'
            candidatura.save()
            
            # Criar registro de Monitor ou MonitorTEA baseado no tipo da vaga
            if tipo_monitoria == 'MonitorTEA':
                # Para MonitorTEA, solicitar salário via POST ou usar valor padrão
                salario = request.POST.get('salario', '1000.00')  # Valor padrão
                MonitorTEA.objects.get_or_create(
                    matricula=candidatura.aluno.matricula,
                    defaults={
                        'nome': candidatura.aluno.nome,
                        'email': candidatura.aluno.email,
                        'telefone': candidatura.aluno.telefone,
                        'senha_hash': candidatura.aluno.senha_hash,
                        'cr_geral': candidatura.aluno.cr_geral,
                        'curso': candidatura.aluno.curso,
                        'salario': salario
                    }
                )
                messages.success(request, f'Candidatura de {candidatura.aluno.nome} aprovada com sucesso! O aluno agora é um Monitor TEA (remunerado).')
            else:
                # Monitor voluntário
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
                messages.success(request, f'Candidatura de {candidatura.aluno.nome} aprovada com sucesso! O aluno agora é um monitor.')
        else:
            # Casa também pode aprovar diretamente
            candidatura.status = 'Aprovada'
            candidatura.save()
            
            # Criar registro de Monitor ou MonitorTEA baseado no tipo da vaga
            if tipo_monitoria == 'MonitorTEA':
                salario = request.POST.get('salario', '1000.00')
                MonitorTEA.objects.get_or_create(
                    matricula=candidatura.aluno.matricula,
                    defaults={
                        'nome': candidatura.aluno.nome,
                        'email': candidatura.aluno.email,
                        'telefone': candidatura.aluno.telefone,
                        'senha_hash': candidatura.aluno.senha_hash,
                        'cr_geral': candidatura.aluno.cr_geral,
                        'curso': candidatura.aluno.curso,
                        'salario': salario
                    }
                )
                messages.success(request, f'Candidatura de {candidatura.aluno.nome} aprovada com sucesso! O aluno agora é um Monitor TEA (remunerado).')
            else:
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
                messages.success(request, f'Candidatura de {candidatura.aluno.nome} aprovada com sucesso! O aluno agora é um monitor.')
    except Exception as e:
        messages.error(request, f'Erro ao aprovar candidatura: {str(e)}')
    
    return redirect('candidaturas_vaga', vaga_id=candidatura.vaga.id)


# Rejeitar Candidatura
def rejeitar_candidatura(request, candidatura_id):
    # Verificar permissão - Apenas professores, coordenadores e casa
    user_type = request.session.get('user_type')
    if user_type not in ['professor', 'coordenador', 'casa']:
        messages.error(request, 'Apenas professores podem rejeitar candidaturas.')
        return redirect('lista_vagas')
    
    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    
    try:
        # Buscar o professor logado
        if user_type in ['professor', 'coordenador']:
            user_cpf = request.session.get('user_id')
            professor = get_object_or_404(Professor, cpf=user_cpf)
            
            # Usar o método do modelo para rejeitar
            professor.rejeitarCandidatura(candidatura)
        else:
            # Casa também pode rejeitar diretamente
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


def detalhes_monitoria(request, monitoria_id):
    """
    Exibe detalhes completos de uma monitoria específica.
    Acessível para Casa, Coordenadores e o próprio Monitor.
    """
    # Verificar autenticação
    if 'user_type' not in request.session:
        return redirect('login')
    
    user_type = request.session.get('user_type')
    
    # Buscar registro de monitoria
    registro = get_object_or_404(RegistroMonitoria, id=monitoria_id)
    
    # Verificar permissão
    if user_type == 'Monitor':
        # Monitor só pode ver suas próprias monitorias
        matricula = request.session.get('user_id')
        if registro.monitor_tea.matricula != matricula:
            return redirect('painel_monitor')
    elif user_type not in ['Casa', 'Coordenador']:
        # Outros tipos de usuário não têm acesso
        return redirect('home')
    
    # Processar lista de alunos participantes
    alunos = registro.alunos_participantes if registro.alunos_participantes else []
    
    # Buscar informações da vaga relacionada
    vaga = registro.monitor_tea.vaga_set.first() if hasattr(registro.monitor_tea, 'vaga_set') else None
    
    context = {
        'registro': registro,
        'alunos': alunos,
        'total_alunos': len(alunos),
        'vaga': vaga,
        'tempo_decorrido': calcular_tempo_decorrido(registro.data_monitoria)
    }
    
    return render(request, 'detalhes_monitoria.html', context)
