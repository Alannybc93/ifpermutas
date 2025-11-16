from django.urls import path
from . import views

app_name = 'core'  # Mantemos o namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('aulas/', views.lista_aulas, name='lista_aulas'),  # ← Mudei para 'aulas/'
    path('minhas-aulas/', views.minhas_aulas, name='minhas_aulas'),
    path('cadastrar-aula/', views.cadastrar_aula, name='cadastrar_aula'),
    path('editar-aula/<int:aula_id>/', views.editar_aula, name='editar_aula'),
    path('excluir-aula/<int:aula_id>/', views.excluir_aula, name='excluir_aula'),
    path('busca-avancada/', views.busca_avancada, name='busca_avancada'),
]