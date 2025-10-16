from django.contrib import admin
from .models import Aluno, Professor, Vaga, Candidatura, RegistroMonitoria

admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Vaga)
admin.site.register(Candidatura)
admin.site.register(RegistroMonitoria)