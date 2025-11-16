from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Professor

@login_required
def profile(request):
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        professor = Professor.objects.create(
            user=request.user,
            matricula=f"MAT-{request.user.id}",
            departamento="A definir",
            campus="A definir"
        )
    return render(request, 'accounts/profile.html', {'professor': professor})

def custom_logout(request):
    logout(request)
    return redirect('accounts:login')