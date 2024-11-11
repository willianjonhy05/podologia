from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo customizado de usuário que herda do AbstractUser.
    Adiciona campos extras, como avatar e pontuação em jogos, para atender
    às necessidades específicas do aplicativo de podologia.
    """
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="Imagem de perfil do usuário.")
    pontuacao_jogos = models.IntegerField(default=0, help_text="Pontuação acumulada do usuário em jogos.")

    # Configuração de related_name para evitar conflitos com o modelo User padrão
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Define um nome alternativo para o relacionamento reverso
        blank=True,
        help_text='Os grupos aos quais este usuário pertence.',
        verbose_name='grupos'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',  # Define um nome alternativo para o relacionamento reverso
        blank=True,
        help_text='Permissões específicas para este usuário.',
        verbose_name='permissões de usuário'
    )

    def __str__(self):
        return self.username

class RelatorioProgresso(models.Model):
    """
    Modelo para armazenar relatórios de progresso de cada usuário.
    Inclui campos para armazenar a data, progresso e recomendações personalizadas.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='relatorios')
    data = models.DateField(auto_now_add=True)
    progresso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentagem de progresso.")
    recomendacoes = models.TextField(blank=True, null=True, help_text="Recomendações de cuidados para o usuário.")

class JogoAtividade(models.Model):
    """
    Modelo para armazenar informações sobre jogos e atividades de usuários.
    Inclui descrição, pontuação e data.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='atividades')
    descricao = models.CharField(max_length=100, help_text="Descrição da atividade ou jogo.")
    pontuacao = models.IntegerField(help_text="Pontuação obtida na atividade.")
    data = models.DateField(auto_now_add=True)

class FeedbackResponsavel(models.Model):
    """
    Modelo para armazenar feedbacks fornecidos pelos responsáveis sobre o atendimento.
    Inclui conteúdo do feedback e data.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='feedbacks')
    conteudo = models.TextField(help_text="Feedback fornecido pelo responsável.")
    data = models.DateField(auto_now_add=True)

class AgendamentoNotificacao(models.Model):
    """
    Modelo para gerenciar agendamentos e notificações de atendimentos.
    Inclui datas de agendamento e notificação.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='agendamentos')
    data_agendamento = models.DateField(help_text="Data do agendamento do atendimento.")
    data_notificacao = models.DateField(help_text="Data para envio da notificação.")
