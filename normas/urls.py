from django.urls import path
from . import views

app_name = 'normas'
urlpatterns = [
    path('busca/', views.exibe_normas, name='exibe_normas'),
    path('conectado/', views.conectado, name='conectado'),
]
