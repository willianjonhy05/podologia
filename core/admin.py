from django.contrib import admin
from .models import Usuario, Disponibilidade, ProfissionalDePodologia, TratamentoPodologico, Agendamento, Feedback

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cpf', 'idade')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('data_nasc',)
    ordering = ('nome',)


@admin.register(Disponibilidade)
class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display = ('dia', 'horario_inicio', 'horario_fim')
    list_filter = ('dia',)
    ordering = ('dia', 'horario_inicio')


@admin.register(ProfissionalDePodologia)
class ProfissionalDePodologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especializacao', 'email', 'telefone_whatsapp', 'aprovado')
    search_fields = ('nome', 'email', 'telefone_whatsapp', 'especializacao')
    list_filter = ('aprovado',)
    ordering = ('nome',)
    filter_horizontal = ('disponibilidade',)


@admin.register(TratamentoPodologico)
class TratamentoPodologicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'preco', 'duracao')
    search_fields = ('nome', 'tipo')
    list_filter = ('tipo',)
    ordering = ('nome',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('data', 'usuario', 'profissional', 'status')
    search_fields = ('usuario__nome', 'profissional__nome')
    list_filter = ('status', 'data')
    ordering = ('data',)
    filter_horizontal = ('servicos',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'agendamento', 'nota', 'data')
    search_fields = ('usuario__nome', 'agendamento__usuario__nome')
    list_filter = ('nota', 'data')
    ordering = ('-data',)
