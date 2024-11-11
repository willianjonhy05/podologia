from rest_framework import serializers
from .models import Usuario, RelatorioProgresso, JogoAtividade, FeedbackResponsavel, AgendamentoNotificacao

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Usuario.
    Transforma instâncias do modelo Usuario em formatos JSON.
    """
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'avatar', 'pontuacao_jogos']

class RelatorioProgressoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo RelatorioProgresso.
    Inclui os campos data, progresso e recomendações para o usuário.
    """
    class Meta:
        model = RelatorioProgresso
        fields = ['id', 'usuario', 'data', 'progresso', 'recomendacoes']

class JogoAtividadeSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo JogoAtividade.
    Inclui os dados de descrição e pontuação das atividades.
    """
    class Meta:
        model = JogoAtividade
        fields = ['id', 'usuario', 'descricao', 'pontuacao', 'data']

class FeedbackResponsavelSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo FeedbackResponsavel.
    Permite que o feedback seja visualizado e adicionado.
    """
    class Meta:
        model = FeedbackResponsavel
        fields = ['id', 'usuario', 'conteudo', 'data']

class AgendamentoNotificacaoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo AgendamentoNotificacao.
    Armazena informações sobre os agendamentos e notificações.
    """
    class Meta:
        model = AgendamentoNotificacao
        fields = ['id', 'usuario', 'data_agendamento', 'data_notificacao']
