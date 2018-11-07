from django.urls import path
from . import views

app_name = 'normas'
urlpatterns = [
    path('', views.conectado, name='conectado'),
    path('fase1', views.fase1, name='fase1'),
    path('empresa/', views.empresa, name='empresa'),
    path('empresa/estrutura', views.estrutura, name='estrutura'),
    path('empresa/estrutura/diretoria', views.estrutura_diretoria, name='estrutura_diretoria'),
    path('empresa/estrutura/empresa', views.estrutura_empresa, name='estrutura_empresa'),
    path('empresa/estrutura/gerencia', views.estrutura_gerencia, name='estrutura_gerencia'),
    path('empresa/estrutura/divisao', views.estrutura_divisao, name='estrutura_divisao'),
    path('empresa/estrutura/areatrab', views.estrutura_areatrab, name='estrutura_areatrab'),
    path('empresa/estrutura/especializacao', views.estrutura_especializacao, name='estrutura_especializacao'),
    path('empresa/estrutura/funcao', views.estrutura_funcao, name='estrutura_funcao'),
    path('empresa/funcionario', views.funcionario, name='funcionario'),
    path('empresa/funcionario/cadastro', views.funcionario_cadastro, name='funcionario_cadastro'),
    path('atividade/', views.atividade, name='atividade'),
    path('atividade/atividade', views.atividade_atividade, name='atividade_atividade'),
    path('atividade/atividade/estrutura', views.atividade_atividade_estrutura, name='atividade_atividade_estrutura'),
    path('atividade/atividade/gerencia', views.atividade_atividade_gerencia, name='atividade_atividade_gerencia'),
    path('atividade/atividade/execucao', views.atividade_atividade_execucao, name='atividade_atividade_execucao'),
    path('atividade/atividade/atividade', views.atividade_atividade_atividade, name='atividade_atividade_atividade'),
    path('atividade/atividade/trabalho', views.atividade_atividade_trabalho, name='atividade_atividade_trabalho'),
    path('atividade/atividade/operacao', views.atividade_atividade_operacao, name='atividade_atividade_operacao'),
    path('atividade/atividade/tarefa', views.atividade_atividade_tarefa, name='atividade_atividade_tarefa'),
    path('exclui/', views.exclui_setor, name='exclui_setor'),
    # generalizar get_info, utilizando o nivel do permissão do usuário requerente.
    path('get_info/diretoria/', views.get_diretorias, name='get_diretorias'),
    path('get_info/empresa/', views.get_empresas, name='get_empresas'),
    path('get_info/gerencia/', views.get_gerencias, name='get_gerencias'),
    path('get_info/divisao/', views.get_divisoes, name='get_divisoes'),
    path('get_info/areatrab/', views.get_areatrabalhos, name='get_areatrabalhos'),
    path('get_info/especialidade/', views.get_especialidades, name='get_especialidades'),
]
