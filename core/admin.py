from django.contrib import admin
from .models import Usuario, RelatorioProgresso, JogoAtividade, FeedbackResponsavel, AgendamentoNotificacao

# Registro dos modelos no Django Admin
admin.site.register(Usuario)
admin.site.register(RelatorioProgresso)
admin.site.register(JogoAtividade)
admin.site.register(AgendamentoNotificacao)

# Registro personalizado do modelo FeedbackResponsavel
@admin.register(FeedbackResponsavel)
class FeedbackResponsavelAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'conteudo', 'data')  # Use 'data' em vez de 'data_criacao'
    search_fields = ('usuario__username', 'conteudo')  # Campos para busca
    list_filter = ('data',)  # Filtros laterais usando 'data'
