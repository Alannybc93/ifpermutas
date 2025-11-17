from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Professor
from core.models import Aula

@login_required
def profile(request):
    """Perfil do professor"""
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        professor = Professor.objects.create(
            user=request.user,
            matricula=f"MAT-{request.user.id}",
            departamento="A definir",
            campus="Principal"
        )
    
    total_aulas = Aula.objects.filter(professor=professor).count()
    aulas_ativas = Aula.objects.filter(professor=professor, status='disponivel').count()
    propostas_pendentes = professor.propostas_recebidas.filter(status='pendente').count()
    notificacoes_nao_lidas = professor.notificacoes.filter(lida=False).count()
    
    context = {
        'professor': professor,
        'total_aulas': total_aulas,
        'aulas_ativas': aulas_ativas,
        'propostas_pendentes': propostas_pendentes,
        'notificacoes_nao_lidas': notificacoes_nao_lidas,
    }
    return render(request, 'accounts/profile.html', context)

from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def custom_logout(request):
    """View personalizada para logout que aceita GET e POST"""
    logout(request)
    return redirect('core:home')