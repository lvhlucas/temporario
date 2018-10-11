from .forms import RequisitaNovoUsuario
from .models import NormaPdf, TitulosNorma
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from normas.tokens import account_activation_token
from django.contrib import messages
from django.http import JsonResponse


def is_authenticated(user):
    return user.is_authenticated


def nivel_1(user):
    return user.groups.filter(name='nivel1').exists()


def nivel_2(user):
    return user.groups.filter(name='nivel2').exists()


def nivel_3(user):
    return user.groups.filter(name='nivel3').exists()


def nivel_logado(user):  # funcionario cadastrado
    return is_authenticated(user) and nivel_1(user)


def nive2_logado(user):  # gerente cadastrado
    return is_authenticated(user) and nivel_2(user)


def nive3_logado(user):  # adm do sistema
    return is_authenticated(user) and nivel_3(user)


def home(request):
    return render(request, 'normasPDF/home.html')


@user_passes_test(nivel_logado, login_url='/login/')
def conectado(request):
    return render(request, 'normasPDF/conectado.html')


@user_passes_test(nivel_logado, login_url='/login/')
def empresa(request):
    # busca todas as empresas e retorna o nome dela
    empresas = {"nome_empresa": [["Empresa A", 55], ["Empresa B", 56]]}

    return render(request, 'normasPDF/empresa.html', {'empresas': empresas})


@user_passes_test(nivel_logado, login_url='/login/')
def exibe_normas(request):
    norma = NormaPdf.objects.select_related('tituloFK').all().order_by('documento', 'tituloFK', 'norma1', 'norma2',
                                                                       'norma3')
    documento = [1, 3, 4]  # buscar o nome de todos os documentos

    return render(request, 'normasPDF/normasPDF.html', {'norma': norma, 'titulo': TitulosNorma.objects.all(),
                                                        'documento': documento})


def get_diretorias(request):
    # buscar no bd todas as diretorias atravez do cod_empresa (request.GET.get("data"))
    resultado = {'diretorias': [['01', 'Diretoria A', 'Diretor A'], ['02', 'Diretoria B', 'Diretor B']]}
    return JsonResponse(resultado)


def get_gerencias(request):
    # buscar no bd todas as gerencias atravez do cod_empresa, cod_diretoria
    resultado = {'gerencias': [['014', 'Gerencia C', 'Gerente C'], ['015', 'Gerencia D', 'Gerente D']]}
    return JsonResponse(resultado)


def get_divisoes(request):
    # buscar no bd todas as divisões atravez do cod_empresa, cod_diretoria, cod_gerencia
    resultado = {'divisoes': [['17', 'Divisão Q', 'Encarregado Q'], ['18', 'Divisão R', 'Encarregado QR']]}
    return JsonResponse(resultado)


def get_areatrabalhos(request):
    # buscar no bd todas as diretorias atravez do cod_empresa (request.GET.get("data"))
    resultado = {'areatrabalhos': [['40', 'Área trabalho T'], ['40', 'Área trabalho U']]}
    return JsonResponse(resultado)


def get_especialidades(request):
    # buscar no bd todas as diretorias atravez do cod_empresa (request.GET.get("data"))
    resultado = {'especialidades': [['21', 'Programador'], ['22', 'Analista']]}
    return JsonResponse(resultado)


def exclui_diretoria(cod_empresa, cod_diretoria):
    # excluir no bd a diretoria passada no parametro
    resposta = ""
    try:
        resposta = "Diretoria excluida com sucesso."
    except:
        resposta = "Houve um problema na excluisão."
    return JsonResponse(resposta)


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura(request):
    return render(request, 'normasPDF/estrutura.html')


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_diretoria(request):
    diretorias = {}

    if request.is_ajax():
        codigo_empresa = request.POST.get('cod_empresa', None)
        # verificar se o codigo da empresa existe, se não retornar mensagem

        # buscar no bd todas as diretorias atravez do codigo_empresa
        diretorias = get_diretorias(codigo_empresa)

        if request.method == "GET":
            # buscar nome da empresa
            nome_empresa = {'nome_empresa': ["nome_1", "nome_2"]}
            return JsonResponse(nome_empresa)

        template = 'normasPDF/tabela.html'
    else:
        template = 'normasPDF/estrutura_diretoria.html'
    return render(request, template, {'setor': diretorias, 'tipo': 'diretoria'})


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_gerencia(request):
    gerencias = {}

    if request.is_ajax():
        codigo_empresa = request.POST.get('cod_empresa', None)
        codigo_diretoria = 0
        # verificar se o codigo da empresa existe, se não retornar mensagem

        # buscar no bd todas as genrecia atravez do codigo_empresa
        gerencias = get_gerencias(codigo_empresa, codigo_diretoria)

        if request.method == "GET":
            # buscar nome da empresa atravez do codigo_empresa
            resposta = {'nome_empresa': ["nome_1", "nome_2"], 'diretorias': get_diretorias(codigo_empresa)}
            return JsonResponse(resposta)

        template = 'normasPDF/tabela.html'
    else:
        template = 'normasPDF/estrutura_gerencia.html'
    return render(request, template, {'setor': gerencias, 'tipo': 'gerencia'})


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_divisao(request):
    return render(request, 'normasPDF/estrutura_divisao.html')


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_areatrab(request):
    return render(request, 'normasPDF/estrutura_areatrab.html')


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_especializacao(request):
    return render(request, 'normasPDF/estrutura_especializacao.html')


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_funcao(request):
    return render(request, 'normasPDF/estrutura_funcao.html')


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_empresa(request):
    return render(request, 'normasPDF/estrutura_empresa.html')


def signup(request):
    if request.method == 'POST':
        form = RequisitaNovoUsuario(request.POST)
        if form.is_valid():  # mudar validação, buscar codigo de empresa
            user = form.save(commit=False)
            user.is_active = False
            user.username = get_random_string(length=6)
            user.save()
            current_site = get_current_site(request)
            origem = "inovetech@gmail.com"
            destino = request.POST['email']  # procurar empresa>pegar gerente>pegar email
            message1 = "Seu pedido de cadastro no sistema Inovetech foi feito com sucesso! Ele ainda deverá avaliado" \
                       " pelo gerente resposavel pela empresa para então poder ser acessado."
            message2 = render_to_string('registration/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            titulo = "Cadastro inovetech."
            user.email_user(titulo, message1)
            send_mail(titulo, message2, origem, [destino], fail_silently=False, )
            return render(request, 'registration/email_send.html')
    else:
        form = RequisitaNovoUsuario()
    return render(request, 'registration/cadastro.html', {'form': form})


@user_passes_test(nive3_logado, login_url='/login/')
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        senha = get_random_string(length=6)
        user.set_password(senha)
        my_group = get_object_or_404(Group, name='nivel1')
        my_group.user_set.add(user)
        user.save()
        titulo = "Acesso liberado na Inovetech"
        message = "usuario:" + user.username + "\nsenha:" + senha + "\nLink para Inovetech:https://" + get_current_site(
            request).domain + "/password"
        user.email_user(titulo, message)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


# recebe pedido de novo funcionario confirma ou não com possibel justificativa, manda para adm validar
@user_passes_test(nive2_logado, login_url='/login/')
def valida_usuario_gerente(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            current_site = get_current_site(request)
            origem = "inovetech@gmail.com"
            destino = "adm@inotech.com"  # email adm do sistema
            message = render_to_string('registration/account_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            titulo = "Cadastro inovetech."
            send_mail(titulo, message, origem, [destino], fail_silently=False, )
        return render(request, 'registration/valida_conta.html', {'usuario': user})
    else:
        return render(request, 'account_activation_invalid.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})
