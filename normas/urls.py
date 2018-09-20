from django.urls import path
from . import views

app_name = 'normas'
urlpatterns = [
    path('busca/', views.exibe_normas, name='exibe_normas'),
    path('', views.conectado, name='conectado'),
    path('empresa/', views.empresa, name='empresa'),
    path('empresa/estrutura', views.estrutura, name='estrutura'),
]
