from django.contrib import admin
from .models import (
    Aluno, Monitor, MonitorTEA, Professor, Coordenador, Casa,
    Disciplina, VagaMonitoria, Candidatura, RegistroMonitoria
)

admin.site.register(Casa)
admin.site.register(Aluno)
admin.site.register(Monitor)
admin.site.register(MonitorTEA)
admin.site.register(Professor)
admin.site.register(Coordenador)
admin.site.register(Disciplina)
admin.site.register(VagaMonitoria)
admin.site.register(Candidatura)
admin.site.register(RegistroMonitoria)