from django import forms
from .models import FeedbackResponsavel, RelatorioProgresso, AgendamentoNotificacao

class FeedbackResponsavelForm(forms.ModelForm):
    class Meta:
        model = FeedbackResponsavel
        fields = ['usuario', 'conteudo']

class RelatorioProgressoForm(forms.ModelForm):
    class Meta:
        model = RelatorioProgresso
        fields = ['usuario', 'progresso', 'recomendacoes']

class AgendamentoNotificacaoForm(forms.ModelForm):
    class Meta:
        model = AgendamentoNotificacao
        fields = ['usuario', 'data_agendamento', 'data_notificacao']