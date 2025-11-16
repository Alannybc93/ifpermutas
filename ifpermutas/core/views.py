from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Aula
from .forms import AulaForm
from accounts.models import Professor
from .forms import AulaForm, BuscaAulaForm 

def home(request):
    """Página inicial do site"""
    # Adicione o contexto que está faltando
    aulas_count = 0
    if request.user.is_authenticated:
        try:
            professor = Professor.objects.get(user=request.user)
            aulas_count = Aula.objects.filter(professor=professor).count()
        except Professor.DoesNotExist:
            # Se o professor não existe, criar automaticamente
            professor = Professor.objects.create(
                user=request.user,
                matricula=f"MAT-{request.user.id}",
                departamento="A definir",
                campus="Principal"
            )
            aulas_count = 0
    
    return render(request, 'core/index.html', {
        'aulas_count': aulas_count
    })
    
@login_required
def lista_aulas(request):
    """Lista todas as aulas disponíveis"""
    aulas = Aula.objects.filter(status='disponivel').select_related('professor__user')
    return render(request, 'core/lista_aulas.html', {'aulas': aulas})

@login_required
def minhas_aulas(request):
    """Aulas cadastradas pelo professor logado"""
    professor = Professor.objects.get(user=request.user)
    aulas = Aula.objects.filter(professor=professor).order_by('-data_criacao')
    return render(request, 'core/minhas_aulas.html', {'aulas': aulas})

@login_required
def cadastrar_aula(request):
    """Cadastrar nova aula"""
    professor = Professor.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            aula = form.save(commit=False)
            aula.professor = professor
            aula.save()
            messages.success(request, 'Aula cadastrada com sucesso!')
            return redirect('core:minhas_aulas')
    else:
        form = AulaForm()
    
    return render(request, 'core/cadastrar_aula.html', {'form': form})

@login_required
def editar_aula(request, aula_id):
    """Editar aula existente"""
    professor = Professor.objects.get(user=request.user)
    aula = get_object_or_404(Aula, id=aula_id, professor=professor)
    
    if request.method == 'POST':
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aula atualizada com sucesso!')
            return redirect('core:minhas_aulas')
    else:
        form = AulaForm(instance=aula)
    
    return render(request, 'core/editar_aula.html', {'form': form, 'aula': aula})

@login_required
def excluir_aula(request, aula_id):
    """Excluir aula"""
    professor = Professor.objects.get(user=request.user)
    aula = get_object_or_404(Aula, id=aula_id, professor=professor)
    
    if request.method == 'POST':
        aula.delete()
        messages.success(request, 'Aula excluída com sucesso!')
        return redirect('core:minhas_aulas')
    
    return render(request, 'core/excluir_aula.html', {'aula': aula})

@login_required
def busca_avancada(request):
    form = BuscaAulaForm(request.GET or None)
    aulas = Aula.objects.filter(status='disponivel').exclude(professor__user=request.user)
    
    if form.is_valid():
        disciplina = form.cleaned_data.get('disciplina')
        campus = form.cleaned_data.get('campus') 
        dia_semana = form.cleaned_data.get('dia_semana')
        turno = form.cleaned_data.get('turno')
        
        if disciplina:
            aulas = aulas.filter(disciplina__icontains=disciplina)
        if campus:
            aulas = aulas.filter(campus__icontains=campus)
        if dia_semana:
            aulas = aulas.filter(dia_semana=dia_semana)
        if turno:
            aulas = aulas.filter(turno=turno)
    
    context = {
        'form': form,
        'aulas': aulas,
        'resultados_count': aulas.count()
    }
    return render(request, 'core/busca_avancada.html', context)