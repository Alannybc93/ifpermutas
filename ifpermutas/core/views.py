from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Aula, PropostaPermuta, Notificacao
from .forms import AulaForm, BuscaAulaForm 
from accounts.models import Professor

def home(request):
    """Página inicial do site"""
    aulas_count = 0
    if request.user.is_authenticated:
        try:
            professor = Professor.objects.get(user=request.user)
            aulas_count = Aula.objects.filter(professor=professor).count()
        except Professor.DoesNotExist:
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

@login_required
def enviar_proposta(request, aula_destino_id):
    """Enviar proposta de permuta para uma aula"""
    professor_origem = Professor.objects.get(user=request.user)
    aula_destino = get_object_or_404(Aula, id=aula_destino_id, status='disponivel')
    
    if aula_destino.professor == professor_origem:
        messages.error(request, "❌ Você não pode fazer permuta com suas próprias aulas!")
        return redirect('core:lista_aulas')
    
    proposta_existente = PropostaPermuta.objects.filter(
        aula_destino=aula_destino,
        professor_origem=professor_origem,
        status='pendente'
    ).exists()
    
    if proposta_existente:
        messages.warning(request, "⚠️ Você já enviou uma proposta para esta aula!")
        return redirect('core:lista_aulas')
    
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem', '')
        aula_origem_id = request.POST.get('aula_origem_id')
        
        if not aula_origem_id:
            messages.error(request, "❌ Selecione uma aula para oferecer em troca!")
            return redirect('core:enviar_proposta', aula_destino_id=aula_destino_id)
        
        aula_origem = get_object_or_404(Aula, id=aula_origem_id, professor=professor_origem)
        
        proposta = PropostaPermuta.objects.create(
            aula_origem=aula_origem,
            aula_destino=aula_destino,
            professor_origem=professor_origem,
            professor_destino=aula_destino.professor,
            mensagem=mensagem,
            status='pendente'
        )
        
        Notificacao.objects.create(
            professor=aula_destino.professor,
            mensagem=f"📨 Nova proposta de permuta recebida de {professor_origem.user.get_full_name()} para a aula de {aula_destino.disciplina}",
            tipo='proposta',
            link=f'/propostas/recebidas/'
        )
        
        messages.success(request, "✅ Proposta enviada com sucesso! Aguarde a resposta do professor.")
        return redirect('core:propostas_enviadas')
    
    aulas_origem = Aula.objects.filter(
        professor=professor_origem, 
        status='disponivel'
    )
    
    context = {
        'aula_destino': aula_destino,
        'aulas_origem': aulas_origem,
    }
    return render(request, 'core/enviar_proposta.html', context)

@login_required
def propostas_recebidas(request):
    """Listar propostas recebidas pelo professor"""
    professor = Professor.objects.get(user=request.user)
    propostas = PropostaPermuta.objects.filter(
        professor_destino=professor
    ).select_related('aula_origem', 'aula_destino', 'professor_origem__user')
    
    Notificacao.objects.filter(
        professor=professor, 
        tipo='proposta', 
        lida=False
    ).update(lida=True)
    
    context = {
        'propostas': propostas,
    }
    return render(request, 'core/propostas_recebidas.html', context)

@login_required
def propostas_enviadas(request):
    """Listar propostas enviadas pelo professor"""
    professor = Professor.objects.get(user=request.user)
    propostas = PropostaPermuta.objects.filter(
        professor_origem=professor
    ).select_related('aula_destino', 'professor_destino__user')
    
    context = {
        'propostas': propostas,
    }
    return render(request, 'core/propostas_enviadas.html', context)

@login_required
def responder_proposta(request, proposta_id, acao):
    """Responder a uma proposta (aceitar/recusar)"""
    professor = Professor.objects.get(user=request.user)
    proposta = get_object_or_404(
        PropostaPermuta, 
        id=proposta_id, 
        professor_destino=professor,
        status='pendente'
    )
    
    if acao == 'aceitar':
        proposta.status = 'aceita'
        mensagem_sucesso = "✅ Proposta aceita com sucesso!"
        
        Notificacao.objects.create(
            professor=proposta.professor_origem,
            mensagem=f"✅ Sua proposta de permuta para {proposta.aula_destino.disciplina} foi aceita!",
            tipo='aceita',
            link=f'/propostas/enviadas/'
        )
        
    elif acao == 'recusar':
        proposta.status = 'recusada'
        mensagem_sucesso = "❌ Proposta recusada."
        
        Notificacao.objects.create(
            professor=proposta.professor_origem,
            mensagem=f"❌ Sua proposta de permuta para {proposta.aula_destino.disciplina} foi recusada.",
            tipo='recusada',
            link=f'/propostas/enviadas/'
        )
    else:
        messages.error(request, "❌ Ação inválida!")
        return redirect('core:propostas_recebidas')
    
    proposta.save()
    messages.success(request, mensagem_sucesso)
    return redirect('core:propostas_recebidas')

@login_required
def notificacoes(request):
    """Listar notificações do professor"""
    professor = Professor.objects.get(user=request.user)
    notificacoes_list = Notificacao.objects.filter(professor=professor)
    
    notificacoes_list.update(lida=True)
    
    context = {
        'notificacoes': notificacoes_list,
    }
    return render(request, 'core/notificacoes.html', context)