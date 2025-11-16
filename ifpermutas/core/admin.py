from django.contrib import admin
from .models import Aula

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['disciplina', 'professor', 'campus', 'dia_semana', 'horario', 'status', 'data_criacao']
    list_filter = ['status', 'tipo', 'campus', 'dia_semana', 'data_criacao']
    search_fields = ['disciplina', 'professor__user__username', 'professor__user__first_name', 'professor__user__last_name']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('professor', 'tipo', 'status')
        }),
        ('Detalhes da Aula', {
            'fields': ('disciplina', 'campus', 'horario', 'dia_semana', 'turma')
        }),
        ('Informações Adicionais', {
            'fields': ('observacoes', 'data_criacao', 'data_atualizacao')
        }),
    )