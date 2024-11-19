from rest_framework import serializers
from .models import Usuario, Disponibilidade, ProfissionalDePodologia, TratamentoPodologico, Agendamento, Feedback

class UsuarioSerializer(serializers.ModelSerializer):
    idade = serializers.ReadOnlyField()

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'data_nasc', 'foto', 'email', 'telefone', 'cpf', 'idade']


class DisponibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidade
        fields = ['id', 'dia', 'horario_inicio', 'horario_fim']


class ProfissionalDePodologiaSerializer(serializers.ModelSerializer):
    disponibilidade = DisponibilidadeSerializer(many=True)
    
    class Meta:
        model = ProfissionalDePodologia
        fields = [
            'id', 'nome', 'especializacao', 'user', 'foto', 'email', 
            'telefone_whatsapp', 'rede_social', 'disponibilidade', 'endereco',
            'bairro', 'especialidade', 'aprovado'
        ]


class TratamentoPodologicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TratamentoPodologico
        fields = ['id', 'nome', 'descricao', 'duracao', 'preco', 'tipo']


class AgendamentoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    profissional = ProfissionalDePodologiaSerializer()
    servicos = TratamentoPodologicoSerializer(many=True)

    class Meta:
        model = Agendamento
        fields = ['id', 'usuario', 'profissional', 'servicos', 'data', 'status']


class FeedbackSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    agendamento = AgendamentoSerializer()

    class Meta:
        model = Feedback
        fields = ['id', 'usuario', 'agendamento', 'nota', 'comentario', 'data']
