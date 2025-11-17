from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['user', 'matricula', 'departamento', 'campus', 'data_cadastro']
    list_filter = ['departamento', 'campus', 'data_cadastro']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'matricula']
    readonly_fields = ['data_cadastro']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Profissionais', {
            'fields': ('matricula', 'departamento', 'campus')
        }),
        ('Contato', {
            'fields': ('telefone',)
        }),
        ('Data', {
            'fields': ('data_cadastro',)
        }),
    )