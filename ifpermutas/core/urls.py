from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Páginas principais
    path('', views.home, name='home'),
    
    # Gestão de Aulas
    path('aulas/', views.lista_aulas, name='lista_aulas'),
    path('minhas-aulas/', views.minhas_aulas, name='minhas_aulas'),
    path('cadastrar-aula/', views.cadastrar_aula, name='cadastrar_aula'),
    path('editar-aula/<int:aula_id>/', views.editar_aula, name='editar_aula'),
    path('excluir-aula/<int:aula_id>/', views.excluir_aula, name='excluir_aula'),
    path('busca-avancada/', views.busca_avancada, name='busca_avancada'),
    
    # Sistema de Propostas
    path('enviar-proposta/<int:aula_destino_id>/', views.enviar_proposta, name='enviar_proposta'),
    path('propostas/recebidas/', views.propostas_recebidas, name='propostas_recebidas'),
    path('propostas/enviadas/', views.propostas_enviadas, name='propostas_enviadas'),
    path('propostas/<int:proposta_id>/<str:acao>/', views.responder_proposta, name='responder_proposta'),
    
    # Sistema de Notificações
    path('notificacoes/', views.notificacoes, name='notificacoes'),
]