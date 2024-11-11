from django.contrib import admin
from django.urls import path, include

# Padrões de URL para o projeto
urlpatterns = [
    path('admin/', admin.site.urls),  # URL para a área de administração do Django
    path('', include('core.urls')),  # Inclui as URLs do app core, incluindo a página inicial

]
