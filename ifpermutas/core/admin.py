from django.contrib import admin
from .models import Aula, PropostaPermuta, Notificacao

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['disciplina', 'professor', 'campus', 'dia_semana', 'turno', 'status', 'data_criacao']
    list_filter = ['status', 'disciplina', 'campus', 'dia_semana', 'turno']
    search_fields = ['professor__user__username', 'professor__user__first_name', 'professor__user__last_name', 'campus']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('professor', 'disciplina', 'campus')
        }),
        ('Horários', {
            'fields': ('dia_semana', 'turno', 'carga_horaria')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PropostaPermuta)
class PropostaPermutaAdmin(admin.ModelAdmin):
    list_display = ['aula_origem', 'aula_destino', 'professor_origem', 'professor_destino', 'status', 'data_proposta']
    list_filter = ['status', 'data_proposta']
    search_fields = [
        'professor_origem__user__username', 
        'professor_destino__user__username',
        'aula_origem__disciplina',
        'aula_destino__disciplina'
    ]
    readonly_fields = ['data_proposta']
    
    fieldsets = (
        ('Proposta', {
            'fields': ('aula_origem', 'aula_destino')
        }),
        ('Professores', {
            'fields': ('professor_origem', 'professor_destino')
        }),
        ('Status e Mensagem', {
            'fields': ('status', 'mensagem')
        }),
        ('Data', {
            'fields': ('data_proposta',)
        }),
    )

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['professor', 'tipo', 'mensagem_curta', 'lida', 'data_criacao']
    list_filter = ['tipo', 'lida', 'data_criacao']
    search_fields = ['professor__user__username', 'mensagem']
    readonly_fields = ['data_criacao']
    
    def mensagem_curta(self, obj):
        return obj.mensagem[:50] + '...' if len(obj.mensagem) > 50 else obj.mensagem
    mensagem_curta.short_description = 'Mensagem'