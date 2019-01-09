from .forms import RequisitaNovoUsuario
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
from normas.models import NormaPDF
from django.http import JsonResponse
import json


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
    return render(request, 'normasPDF/base.html')


@user_passes_test(nivel_logado, login_url='/login/')
def fase1(request):
    return render(request, 'normasPDF/fase1.html')


@user_passes_test(nivel_logado, login_url='/login/')
def empresa(request):
    # busca todas as empresas e retorna o nome dela
    empresas = {"nome_empresa": [["Empresa A", 55], ["Empresa B", 56]]}

    return render(request, 'normasPDF/empresa.html', {'empresas': empresas})


def get_nivel1(request):
    resultado = {}
    # falta verificar o nivel de segurança do usuário.
    # fazer a buscar no banco de dados para cada setor utilizando request.GET.get("data") como paramentro
    # resultado esperado para retorno {"nomesetor":[['id','nome'],['id',nome']]}
    if request.GET.get("tipo") == "empresa":
        resultado = {'empresas': [['01', 'Empresa H', 'Dono H'], ['02', 'Empresa J', 'Dono J']]}
    elif request.GET.get("tipo") == "diretoria":
        resultado = {'diretorias': [['01', 'Diretoria A', 'Diretor A'], ['02', 'Diretoria B', 'Diretor B']]}
    elif request.GET.get("tipo") == "gerencia":
        resultado = {'gerencias': [['014', 'Gerencia C', 'Gerente C'], ['015', 'Gerencia D', 'Gerente D']]}
    elif request.GET.get("tipo") == "divisao":
        resultado = {'divisoes': [['17', 'Divisão Q', 'Encarregado Q'], ['18', 'Divisão R', 'Encarregado QR']]}
    elif request.GET.get("tipo") == "areatrabalho":
        resultado = {'areatrabalhos': [['40', 'Área trabalho T'], ['40', 'Área trabalho U']]}
    elif request.GET.get("tipo") == "especialidade":
        resultado = {'especialidades': [['21', 'Programador'], ['22', 'Analista']]}
    elif request.GET.get("tipo") == "funcao":
        resultado = {'funcoes': [['21', 'X'], ['22', 'C']]}

    return JsonResponse(resultado)


def exclui_nivel1(request):
    try:
        # excluir no bd o dado passada no parametro
        resposta = "Setor excluido com sucesso."
    except:
        resposta = "Houve um problema na excluisão."
    return JsonResponse(resposta)


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura(request):
    return render(request, 'normasPDF/empresa_estrutura.html')


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_empresa(request):
    conteudo = "empresa"
    template = 'normasPDF/empresa_estrutura_empresa.html'

    return render(request, template, {'setor': json.loads(get_nivel1(conteudo).content), 'tipo': 'Empresa'})


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_diretoria(request):
    conteudo = "diretoria"
    template = 'normasPDF/empresa_estrutura_diretoria.html'

    return render(request, template, {'setor': json.loads(get_nivel1(conteudo).content), 'tipo': 'diretoria'})


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_gerencia(request):
    conteudo = "gerencia"
    template = 'normasPDF/empresa_estrutura_gerencia.html'

    return render(request, template,
                  {'setor': json.loads(get_nivel1(conteudo).content), 'tipo': 'gerencia'})


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_divisao(request):
    conteudo = "divisao"
    template = 'normasPDF/empresa_estrutura_divisao.html'

    return render(request, template,
                  {'setor': json.loads(get_nivel1(conteudo).content), 'tipo': 'divisões'})


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_areatrab(request):
    conteudo = "areatrabalho"
    template = 'normasPDF/empresa_estrutura_areatrab.html'

    return render(request, template,
                  {'setor': json.loads(get_nivel1(conteudo).content), 'tipo': 'Área de trabalhos'})


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_especializacao(request):
    conteudo = "especialidade"
    template = 'normasPDF/empresa_estrutura_especializacao.html'

    return render(request, template,
                  {'setor': json.loads(get_nivel1(conteudo).content), 'tipo': 'especialidades'})


@user_passes_test(nivel_logado, login_url='/login/')
def estrutura_funcao(request):
    conteudo = "funcao"
    template = 'normasPDF/empresa_estrutura_funcao.html'

    return render(request, template, {'setor': json.loads(get_nivel1(conteudo).content), 'tipo': 'Funções'})


@user_passes_test(nivel_logado, login_url='/login/')
def funcionario(request):
    template = 'normasPDF/funcionario.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def funcionario_cadastro(request):
    template = 'normasPDF/funcionario_cadastro.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def atividade(request):
    template = 'normasPDF/atividade.html'
    empresas = {"nome_empresa": [["Empresa A", 55], ["Empresa B", 56]]}
    return render(request, template, {"empresa": empresas})


@user_passes_test(nivel_logado, login_url='/login/')
def atividade_atividade(request):
    template = 'normasPDF/atividade_atividade.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def atividade_atividade_estrutura(request):
    template = 'normasPDF/atividade_atividade_estrutura.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def atividade_atividade_gerencia(request):
    template = 'normasPDF/atividade_atividade_gerencia.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def atividade_atividade_execucao(request):
    template = 'normasPDF/atividade_atividade_execucao.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def atividade_atividade_atividade(request):
    template = 'normasPDF/atividade_atividade_atividade.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def atividade_atividade_trabalho(request):
    template = 'normasPDF/atividade_atividade_trabalho.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def atividade_atividade_operacao(request):
    template = 'normasPDF/atividade_atividade_operacao.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def atividade_atividade_tarefa(request):
    template = 'normasPDF/atividade_atividade_tarefa.html'
    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos(request):
    template = "normasPDF/normasprocedimentos.html"

    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_normas(request):
    template = 'normasPDF/normasprocedimentos_normas.html'
    try:
        queryfromdatabase = NormaPDF.objects.all()
        resposta = ""
    except:  # especificar o except. falha ao conectar ao banco de dados
        resposta = "Falha ao comuniar com o banco de dados"
    return render(request, template, {'resultado': queryfromdatabase, 'sucesso': resposta})


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_procedimentos(request):
    template = 'normasPDF/normasprocedimentos_procedimentos.html'

    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_estudos(request):
    template = 'normasPDF/normasprocedimentos_estudos.html'

    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_referencias(request):
    template = 'normasPDF/normasprocedimentos_referencias.html'

    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_referencias_gerencia(request):
    template = 'normasPDF/normasprocedimentos_referencias_gerencia.html'

    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_referencias_atividade(request):
    template = 'normasPDF/normasprocedimentos_referencias_atividade.html'

    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_referencias_operacao(request):
    template = 'normasPDF/normasprocedimentos_referencias_operacao.html'

    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_referencias_tipo(request):
    template = 'normasPDF/normasprocedimentos_referencias_tipo.html'

    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_referencias_assunto(request):
    template = 'normasPDF/normasprocedimentos_referencias_assunto.html'

    return render(request, template)


@user_passes_test(nivel_logado, login_url='/login/')
def normasprocedimentos_referencias_glossario(request):
    template = 'normasPDF/normasprocedimentos_referencias_glossario.html'

    return render(request, template)


def signup(request):
    if request.method == 'POST':
        form = RequisitaNovoUsuario(request.POST)
        if form.is_valid():  # mudar validação, buscando codigo de empresa
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
