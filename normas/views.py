from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import NormaPdf, TitulosNorma
from django.urls import reverse
from django.http import HttpResponseRedirect


def is_authenticated(user):
    return user.is_authenticated


def nivel_1(user):
    return user.groups.filter(name='nivel1').exists()


def nivel_2(user):
    return user.groups.filter(name='nivel1').exists()


def nivel_3(user):
    return user.groups.filter(name='nivel1').exists()


def nivel_logado(user):
    return is_authenticated(user) and nivel_1(user)


def nive2_logado(user):
    return is_authenticated(user) and nivel_1(user)


def nive3_logado(user):
    return is_authenticated(user) and nivel_1(user)


def home(request):
    return render(request, 'normasPDF/home.html')


@user_passes_test(nivel_logado, login_url='/login/')
def conectado(request):
    return render(request, 'normasPDF/conectado.html')


@user_passes_test(nivel_logado, login_url='/login/')
def exibe_normas(request):
    norma = NormaPdf.objects.select_related('tituloFK').all().order_by('documento', 'tituloFK', 'norma1', 'norma2',
                                                                       'norma3')
    documento = [1]

    return render(request, 'normasPDF/normasPDF.html', {'norma': norma, 'titulo': TitulosNorma.objects.all(),
                                                        'documento': documento})


