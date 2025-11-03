from django.contrib import admin
from .models import (
    Aluno, Monitor, MonitorTEA, Professor, Coordenador,
    Disciplina, VagaMonitoria, Candidatura, RegistroAtividadeMonitoria
)

admin.site.register(Aluno)
admin.site.register(Monitor)
admin.site.register(MonitorTEA)
admin.site.register(Professor)
admin.site.register(Coordenador)
admin.site.register(Disciplina)
admin.site.register(VagaMonitoria)
admin.site.register(Candidatura)
admin.site.register(RegistroAtividadeMonitoria)