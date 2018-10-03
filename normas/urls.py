from django.urls import path
from . import views

app_name = 'normas'
urlpatterns = [
    path('busca/', views.exibe_normas, name='exibe_normas'),
    path('', views.conectado, name='conectado'),
    path('empresa/', views.empresa, name='empresa'),
    path('empresa/estrutura', views.estrutura, name='estrutura'),
    path('empresa/estrutura/diretoria', views.estrutura_diretoria, name='estrutura_diretoria'),
    path('empresa/estrutura/empresa', views.estrutura_empresa, name='estrutura_empresa'),
    path('empresa/estrutura/gerencia', views.estrutura_gerencia, name='estrutura_gerencia'),
    path('empresa/estrutura/divisao', views.estrutura_divisao, name='estrutura_divisao'),
    path('empresa/estrutura/areatrab', views.estrutura_areatrab, name='estrutura_areatrab'),
    path('empresa/estrutura/especializacao', views.estrutura_especializacao, name='estrutura_especializacao'),
    path('empresa/estrutura/funcao', views.estrutura_funcao, name='estrutura_funcao'),
]
