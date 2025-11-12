from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import date


# Base para todos os usuários
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=15)
    senha_hash = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def login(self):
        raise NotImplementedError("Método login() deve ser implementado")

    def logout(self):
        raise NotImplementedError("Método logout() deve ser implementado")

    def alterarSenha(self, nova_senha):
        self.senha_hash = make_password(nova_senha)
        self.save()
        return True


class Aluno(Usuario):
    matricula = models.CharField(max_length=12, unique=True, primary_key=True)
    cr_geral = models.FloatField()
    curso = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.matricula} - {self.nome}"

    def buscarVaga(self, disciplina):
        return VagaMonitoria.objects.filter(disciplina=disciplina, status='Aberta')

    def realizarCandidatura(self, vagaMonitoria):
        return Candidatura.objects.create(
            aluno=self,
            vaga=vagaMonitoria,
            status='Pendente'
        )


class Monitor(Aluno):
    class Meta:
        verbose_name = 'Monitor'
        verbose_name_plural = 'Monitores'

 



# Monitoria remunerada
class MonitorTEA(Aluno):
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Monitor TEA'
        verbose_name_plural = 'Monitores TEA'

    def gerenciarDisponibilidade(self, horario):
        horarios = [
            {"dia": "Segunda", "inicio": "12:00", "fim": "13:00"},
            {"dia": "Terça", "inicio": "12:00", "fim": "13:00"},
            {"dia": "Quarta", "inicio": "12:00", "fim": "13:00"},
            {"dia": "Quinta", "inicio": "12:00", "fim": "13:00"},
            {"dia": "Sexta", "inicio": "12:00", "fim": "13:00"}
        ]

        horario_escolhido = []

        for horario in horarios:
            horario_escolhido.append(horario)
        
        return horario_escolhido

    def submeterRelatorioHoras(self, registro):
        if hasattr(registro, 'submeter'):
            return registro.submeter()
        raise ValueError("Registro inválido")

    def __str__(self):
        return f"MonitorTEA {self.matricula} - Salário: R$ {self.salario}"


# Professor da instituição
class Professor(Usuario):
    cpf = models.CharField(max_length=14, unique=True, primary_key=True)

    def aprovarCandidatura(self, candidatura):
        """Professor pode aprovar candidatura de monitoria"""
        candidatura.status = 'Aprovada'
        candidatura.save()
        
        # Criar registro de Monitor se ainda não existir
        try:
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
        except Exception as e:
            print(f"Erro ao criar monitor: {e}")
        
        return candidatura
    
    def rejeitarCandidatura(self, candidatura):
        """Professor pode rejeitar candidatura de monitoria"""
        candidatura.status = 'Rejeitada'
        candidatura.save()
        return candidatura

    def __str__(self):
        return f"{self.cpf} - {self.nome}"


class Coordenador(Professor):
    class Meta:
        verbose_name = 'Coordenador'
        verbose_name_plural = 'Coordenadores'

    def cadastrarVaga(self, vaga):
        vaga.save()
        return vaga

    def __str__(self):
        return f"Coordenador {self.cpf} - {self.nome}"


# Administrador do sistema
class Casa(Usuario):
    class Meta:
        verbose_name = 'Casa (Administrador)'
        verbose_name_plural = 'Casa (Administradores)'

    def cadastrarCoordenador(self, coordenador_data):
        coordenador = Coordenador(**coordenador_data)
        coordenador.save()
        return coordenador

    def cadastrarVaga(self, vaga):
        vaga.save()
        return vaga

    def __str__(self):
        return f"Casa - {self.nome}"

    
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class VagaMonitoria(models.Model):
    titulo = models.CharField(max_length=100)
    pre_requisitos = models.TextField()
    disciplina = models.ForeignKey(
        'Disciplina',
        on_delete=models.CASCADE,
        related_name='vagas'
    )
    coordenador = models.ForeignKey(
        'Coordenador',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='vagas_cadastradas'
    )
    casa = models.ForeignKey(
        'Casa',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='vagas_criadas'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Aberta', 'Aberta'),
            ('Fechada', 'Fechada'),
            ('Em Análise', 'Em Análise')
        ],
        default='Aberta'
    )
    tipo_monitoria = models.CharField(
        max_length=20,
        choices=[
            ('Monitor', 'Monitor (Voluntário)'),
            ('MonitorTEA', 'Monitor TEA (Remunerado)')
        ],
        default='Monitor',
        help_text="Tipo de monitoria: Monitor voluntário ou Monitor TEA remunerado"
    )
    prazo_inscricao = models.DateField()

    def __str__(self):
        return f"{self.titulo} - {self.disciplina.nome}"

    def verDetalhes(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'pre_requisitos': self.pre_requisitos,
            'disciplina': str(self.disciplina),
            'status': self.status,
            'prazo_inscricao': self.prazo_inscricao.isoformat() if self.prazo_inscricao else None,
        }

    def visualizarCandidaturas(self):
        return self.candidaturas_recebidas.all()


class Candidatura(models.Model):
    documentos = models.TextField()
    cr_disciplina = models.FloatField(default=0.0, help_text="CR (Coeficiente de Rendimento) na disciplina da vaga")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pendente', 'Pendente'),
            ('Aprovada', 'Aprovada'),
            ('Rejeitada', 'Rejeitada')
        ],
        default='Pendente'
    )
    data_candidatura = models.DateField(default=date.today)
    aluno = models.ForeignKey(
        'Aluno',
        on_delete=models.CASCADE,
        related_name='candidaturas_realizadas'
    )
    vaga = models.ForeignKey(
        'VagaMonitoria',
        on_delete=models.CASCADE,
        related_name='candidaturas_recebidas'
    )

    def validarCR(self) -> bool:
        return self.aluno.cr_geral >= 7.0 and self.cr_disciplina >= 8.0

    def submeter(self):
        self.status = 'Pendente'
        self.save()
        return self

    def cancelar(self):
        self.status = 'Rejeitada'
        self.save()
        return self

    def __str__(self):
        return f"Candidatura de {self.aluno.nome} para {self.vaga.titulo} - {self.status}"


class RegistroMonitoria(models.Model):
    data_monitoria = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    horas_trabalhadas = models.DecimalField(max_digits=4, decimal_places=2)
    codigo_disciplina = models.CharField(max_length=20)
    descricao_atividade = models.TextField(help_text="O que foi ensinado/abordado na monitoria")
    alunos_participantes = models.JSONField(
        default=list,
        help_text="Lista de dicionários com 'matricula' e 'nome' dos alunos participantes"
    )
    quantidade_alunos = models.IntegerField(default=0)
    data_registro = models.DateField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)
    
    monitor_tea = models.ForeignKey(
        'MonitorTEA',
        on_delete=models.CASCADE,
        related_name='registros_monitorias'
    )
    candidatura = models.ForeignKey(
        'Candidatura',
        on_delete=models.CASCADE,
        related_name='registros_atividade'
    )

    class Meta:
        verbose_name = 'Registro de Monitoria'
        verbose_name_plural = 'Registros de Monitoria'
        ordering = ['-data_monitoria']

    def submeter(self):
        self.save()
        return self

    def visualizarDetalhes(self):
        return {
            'id': self.id,
            'monitor': str(self.monitor_tea),
            'data_monitoria': self.data_monitoria.isoformat(),
            'horario': f"{self.horario_inicio} - {self.horario_fim}",
            'horas_trabalhadas': float(self.horas_trabalhadas),
            'codigo_disciplina': self.codigo_disciplina,
            'descricao_atividade': self.descricao_atividade,
            'alunos_participantes': self.alunos_participantes,
            'quantidade_alunos': self.quantidade_alunos,
            'observacoes': self.observacoes,
        }

    def __str__(self):
        return f"Monitoria {self.data_monitoria} - {self.monitor_tea.nome} - {self.quantidade_alunos} alunos"
