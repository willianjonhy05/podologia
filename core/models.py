from django.db import models
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError


class Usuario(models.Model):
    nome = models.CharField('Nome', max_length=255)
    data_nasc = models.DateField('Data de Nascimento', null=True, blank=True)
    foto = models.ImageField("Foto", upload_to='avatares', blank=True, null=True)
    email = models.EmailField('E-mail')
    telefone = models.CharField("Telefone", max_length=15, null=True, blank=True)
    cpf = models.CharField("CPF", max_length=15, null=True, blank=True)
    user = models.OneToOneField(
        get_user_model(),
        verbose_name="Usuário",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="usuario"
    )

    @property
    def idade(self):
        if self.data_nasc:
            hoje = date.today()
            diferenca = hoje - self.data_nasc
            return round(diferenca.days // 365.25)
        return None

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Disponibilidade(models.Model):
    DIAS_DA_SEMANA = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    dia = models.CharField(
        max_length=10,
        choices=DIAS_DA_SEMANA,
        verbose_name="Dia da Semana"
    )
    horario_inicio = models.TimeField(verbose_name="Horário de Início")
    horario_fim = models.TimeField(verbose_name="Horário de Fim")

    class Meta:
        verbose_name = "Disponibilidade"
        verbose_name_plural = "Disponibilidades"
        ordering = ['dia', 'horario_inicio']

    def __str__(self):
        return f"{self.get_dia_display()} ({self.horario_inicio} às {self.horario_fim})"

    def clean(self):
        if self.horario_inicio >= self.horario_fim:
            raise ValidationError("O horário de fim deve ser posterior ao horário de início.")


class ProfissionalDePodologia(models.Model):
    nome = models.CharField("Nome", max_length=100)
    especializacao = models.CharField(
        max_length=300,
        help_text="Especialização, como atendimento infantil, TEA/TDAH etc."
    )
    user = models.OneToOneField(
        get_user_model(),
        verbose_name="Usuário",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="profissional"
    )
    foto = models.ImageField("Foto", upload_to='avatares', blank=True, null=True)
    email = models.EmailField("E-mail", help_text="E-mail de contato do profissional")
    telefone_whatsapp = models.CharField(
        "Telefone/WhatsApp",
        max_length=15,
        null=True,
        blank=True,
        help_text="Telefone de contato"
    )
    rede_social = models.URLField(
        "Link de Rede Social",
        null=True,
        blank=True,
        help_text="Website ou página de contato do profissional"
    )
    disponibilidade = models.ManyToManyField(
        Disponibilidade,
        verbose_name="Disponibilidades",
        related_name="profissionais"
    )
    endereco = models.CharField(
        "Endereço",
        max_length=255,
        null=True,
        blank=True,
        help_text="Endereço"
    )
    bairro = models.CharField(
        "Bairro",
        max_length=255,
        null=True,
        blank=True,
        help_text="Bairro"
    )
    especialidade = models.TextField(
        "Especialidade",
        help_text="Descrição da especialidade do profissional e sua experiência"
    )
    aprovado = models.BooleanField("Aprovado", default=False)

    class Meta:
        verbose_name = "Profissional de Podologia"
        verbose_name_plural = "Profissionais de Podologia"

    def __str__(self):
        return self.nome


class TratamentoPodologico(models.Model):
    TIPOS_TRATAMENTO = [
        ('Preventivo', 'Preventivo'),
        ('Estético', 'Estético'),
        ('Clínico', 'Clínico'),
        ('Reabilitação', 'Reabilitação'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome do Tratamento")
    descricao = models.TextField(verbose_name="Descrição", help_text="Breve descrição do tratamento.")
    duracao = models.PositiveIntegerField(verbose_name="Duração (minutos)", help_text="Duração média do tratamento.")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    tipo = models.CharField(max_length=20, choices=TIPOS_TRATAMENTO, verbose_name="Tipo do Tratamento")

    class Meta:
        verbose_name = "Tratamento Podológico"
        verbose_name_plural = "Tratamentos Podológicos"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Cliente", related_name="agendamentos")
    profissional = models.ForeignKey(
        ProfissionalDePodologia, on_delete=models.CASCADE, verbose_name="Profissional", related_name="agendamentos"
    )
    servicos = models.ManyToManyField(TratamentoPodologico, verbose_name="Serviços", related_name="agendamentos")
    data = models.DateField(verbose_name="Data do Agendamento", default=date.today)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status do Agendamento"
    )

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['data']

    def __str__(self):
        return f"Agendamento em {self.data} - {self.usuario.nome}"

    def marcar_concluido(self):
        self.status = 'concluido'
        self.save()

    def cancelar(self):
        self.status = 'cancelado'
        self.save()



class Feedback(models.Model):
    NOTA_CHOICES = [
        (1, '1 - Muito ruim'),
        (2, '2 - Ruim'),
        (3, '3 - Regular'),
        (4, '4 - Bom'),
        (5, '5 - Excelente'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name="Cliente",
        related_name="feedbacks"
    )
    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.CASCADE,
        verbose_name="Agendamento",
        related_name="feedback"
    )
    nota = models.PositiveSmallIntegerField(
        choices=NOTA_CHOICES,
        verbose_name="Nota",
        help_text="Nota de 1 a 5 sobre o atendimento"
    )
    comentario = models.TextField(
        verbose_name="Comentário",
        blank=True,
        null=True,
        help_text="Comentários adicionais sobre o atendimento"
    )
    data = models.DateTimeField(
        verbose_name="Data do Feedback",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-data']

    def __str__(self):
        return f"Feedback de {self.usuario.nome} - Nota: {self.nota}"

    def clean(self):
        """
        Validações adicionais:
        - Garante que o agendamento já foi concluído antes de receber feedback.
        """
        if self.agendamento.status != 'concluido':
            raise ValidationError("O feedback só pode ser enviado para atendimentos concluídos.")





############################################################################################################

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
    

class Usuario(models.Model):
    nome = models.CharField('Nome', max_length=255)
    data_nasc = models.DateField('Data de Nascimento', null=True, blank=True)
    foto = models.ImageField("Foto", upload_to='avatares', blank=True, null=True)
    email = models.EmailField('E-mail')
    telefone = models.CharField("Telefone", max_length=15, null=True, blank=True)
    cpf = models.CharField("CPF", max_length=15, null=True, blank=True)
    user = models.OneToOneField(get_user_model(), verbose_name="Usuário", on_delete=models.CASCADE, null=True, blank=True, related_name="usuario")

    @property
    def idade(self):
        hoje = date.today()
        diferenca = hoje - self.data_nasc
        return round(diferenca.days // 365.25)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

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
