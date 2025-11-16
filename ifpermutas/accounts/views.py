from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Professor

@require_http_methods(["GET", "POST"])
def custom_logout(request):
    """View personalizada para logout que aceita GET e POST"""
    logout(request)
    return redirect('core:home')  # Redireciona para a home após logout

@login_required
def profile(request):
    """Perfil do professor"""
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        # Criar professor automaticamente se não existir
        professor = Professor.objects.create(
            user=request.user,
            matricula=f"MAT-{request.user.id}",
            departamento="A definir",
            campus="Principal"
        )
    
    # Contar aulas do professor
    from core.models import Aula
    total_aulas = Aula.objects.filter(professor=professor).count()
    aulas_ativas = Aula.objects.filter(professor=professor, status='disponivel').count()
    
    context = {
        'professor': professor,
        'total_aulas': total_aulas,
        'aulas_ativas': aulas_ativas,
    }
    return render(request, 'accounts/profile.html', context)