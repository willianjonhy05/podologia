from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

# Roteador para as APIs
router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet, basename='usuario')
router.register(r'relatorios', views.RelatorioProgressoViewSet, basename='relatorio')
router.register(r'atividades', views.JogoAtividadeViewSet, basename='atividade')
router.register(r'feedbacks', views.FeedbackResponsavelViewSet, basename='feedback')
router.register(r'agendamentos', views.AgendamentoNotificacaoViewSet, basename='agendamento')

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('dashboard/', views.dashboard, name='dashboard'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/adicionar/', views.adicionar_relatorio, name='adicionar_relatorio'),

    # Rotas para Feedbacks
    path('feedbacks/', views.listar_feedbacks, name='listar_feedbacks'),
    path('feedbacks/adicionar/', views.adicionar_feedback, name='adicionar_feedback'),
    path('feedbacks/editar/<int:pk>/', views.editar_feedback, name='editar_feedback'),
    path('feedbacks/excluir/<int:pk>/', views.excluir_feedback, name='excluir_feedback'),

    # Rotas para Agendamentos
    path('agendamentos/', views.agendamentos, name='agendamentos'),
    path('agendamentos/adicionar/', views.adicionar_agendamento, name='adicionar_agendamento'),

    # Endpoints de autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Login
    path('login/', views.login_view, name='login'),

    # Inclui as rotas do roteador para as APIs
    path('api/', include(router.urls)),
]
