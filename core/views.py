from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Usuario, RelatorioProgresso, JogoAtividade, FeedbackResponsavel, AgendamentoNotificacao, FeedbackResponsavel
from .serializers import UsuarioSerializer, RelatorioProgressoSerializer, JogoAtividadeSerializer, FeedbackResponsavelSerializer, AgendamentoNotificacaoSerializer
from .forms import FeedbackResponsavelForm, RelatorioProgressoForm, AgendamentoNotificacaoForm

# Views para renderizar os templates

def home(request):
    """
    View para a página inicial do aplicativo.
    """
    return render(request, 'dashboard.html')  # Página inicial

def login_view(request):
    """
    View para a página de login.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redireciona para o dashboard após o login
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})
    return render(request, 'login.html')

@login_required
def dashboard(request):
    """
    View para o painel do administrador.
    """
    return render(request, 'dashboard.html')

@login_required
def relatorios(request):
    """
    View para a página de relatórios de progresso.
    Exibe todos os relatórios de progresso para o usuário atual.
    """
    relatorios = RelatorioProgresso.objects.filter(usuario=request.user)
    return render(request, 'relatorios.html', {'relatorios': relatorios})

@login_required
def feedbacks(request):
    """
    View para a página de feedbacks dos responsáveis.
    Exibe todos os feedbacks fornecidos para o usuário atual.
    """
    feedbacks = FeedbackResponsavel.objects.filter(usuario=request.user)
    return render(request, 'feedbacks.html', {'feedbacks': feedbacks})

@login_required
def agendamentos(request):
    """
    View para a página de agendamentos.
    Exibe todos os agendamentos para o usuário atual.
    """
    agendamentos = AgendamentoNotificacao.objects.filter(usuario=request.user)
    return render(request, 'agendamentos.html', {'agendamentos': agendamentos})

def listar_feedbacks(request):
    feedbacks = FeedbackResponsavel.objects.all()
    return render(request, 'feedback/listar_feedbacks.html', {'feedbacks': feedbacks})

def adicionar_feedback(request):
    if request.method == 'POST':
        form = FeedbackResponsavelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_feedbacks')
    else:
        form = FeedbackResponsavelForm()
    return render(request, 'feedback/adicionar_feedback.html', {'form': form})

def editar_feedback(request, pk):
    feedback = get_object_or_404(FeedbackResponsavel, pk=pk)
    if request.method == 'POST':
        form = FeedbackResponsavelForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('listar_feedbacks')
    else:
        form = FeedbackResponsavelForm(instance=feedback)
    return render(request, 'feedback/editar_feedback.html', {'form': form})

def excluir_feedback(request, pk):
    feedback = get_object_or_404(FeedbackResponsavel, pk=pk)
    if request.method == 'POST':
        feedback.delete()
        return redirect('listar_feedbacks')
    return render(request, 'feedback/excluir_feedback.html', {'feedback': feedback})

@login_required
def adicionar_relatorio(request):
    if request.method == 'POST':
        form = RelatorioProgressoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relatorios')  # Redireciona para a lista de relatórios após adicionar
    else:
        form = RelatorioProgressoForm()
    return render(request, 'relatorios/adicionar_relatorio.html', {'form': form})

@login_required
def adicionar_agendamento(request):
    """
    View para adicionar um novo agendamento.
    """
    if request.method == 'POST':
        form = AgendamentoNotificacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agendamentos')  # Redireciona para a lista de agendamentos após adicionar
    else:
        form = AgendamentoNotificacaoForm()
    return render(request, 'agendamentos/adicionar_agendamento.html', {'form': form})

# ViewSets para API

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo Usuario.
    Permite listar, criar, atualizar e excluir usuários via API.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class RelatorioProgressoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo RelatorioProgresso.
    Usado para gerenciar relatórios de progresso.
    """
    queryset = RelatorioProgresso.objects.all()
    serializer_class = RelatorioProgressoSerializer

class JogoAtividadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo JogoAtividade.
    Usado para gerenciar atividades e pontuações dos usuários.
    """
    queryset = JogoAtividade.objects.all()
    serializer_class = JogoAtividadeSerializer

class FeedbackResponsavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo FeedbackResponsavel.
    Permite aos responsáveis fornecer e gerenciar feedbacks.
    """
    queryset = FeedbackResponsavel.objects.all()
    serializer_class = FeedbackResponsavelSerializer

class AgendamentoNotificacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo AgendamentoNotificacao.
    Usado para gerenciar agendamentos e notificações.
    """
    queryset = AgendamentoNotificacao.objects.all()
    serializer_class = AgendamentoNotificacaoSerializer
