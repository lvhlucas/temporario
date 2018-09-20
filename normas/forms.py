from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Empresa, Funcionario


class RequisitaNovoUsuario(forms.ModelForm):
    empresa = forms.CharField(max_length=10)
    first_name = forms.CharField(label="Primeiro Nome")
    last_name = forms.CharField(label="Sobrenome")
    empresa = forms.CharField(label="Código da empresa")
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'empresa')
