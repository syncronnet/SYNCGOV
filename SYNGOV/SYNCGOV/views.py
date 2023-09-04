import json
import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.urls import path
from .import views
from .populacao import obter_dados_ibge, calcular_populacao_total, calcular_diferenca


# Criar views aqui.

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def index(request):
    return verifica_login(request, 'index.html')
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def cadastro(request):
    if request.method == 'POST':
        try:
            usuario_aux = User.objects.get(username=request.POST['username'])
            if usuario_aux:
                messages.error(request, 'Já temos esse usuário cadastrado.')
                return redirect('cadastro')
        except User.DoesNotExist:
            nome_usuario = request.POST['username']
            email = request.POST['email']
            senha = request.POST['password']
            novoUsuario = User.objects.create_user(username=nome_usuario, email=email, password=senha)
            novoUsuario.save()
            return redirect_mensagem(0, 'index', request, 'Cadastro realizado com sucesso.')
            

    return verifica_login(request, 'cadastro.html')

@csrf_exempt
#@api_view(["POST"])
@permission_classes((AllowAny,))
def principal(request):
    return render(request, 'principal.html')
# Lista de frases de boas-vindas
frases_boas_vindas = [
    "Bem-vindo de volta!",
    "Ótimo ver você novamente!",
    "Seja bem-vindo ao nosso sistema!",
    "Esperamos que tenha um ótimo dia!",
    "Que bom tê-lo de volta!",
    "Saudações!",
    "Você está conectado!",
    "Bem-vindo ao nosso portal!",
    "Estamos felizes em vê-lo novamente!",
    "Aproveite o seu tempo aqui!"
]

# Função para obter uma frase de boas-vindas aleatória
def obter_frase_boas_vindas():
    return random.choice(frases_boas_vindas)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logar(request):
    try:
        usuario_aux = User.objects.get(username=request.POST['username'])
        usuario = authenticate(username=usuario_aux.username,
                               password=request.POST["password"])
        if usuario is not None:
            try:
                login(request, usuario)
                mensagem_boas_vindas = obter_frase_boas_vindas()
                # Adicione a mensagem de boas-vindas às mensagens
                return render(request, 'principal.html', {'mensagem_boas_vindas': mensagem_boas_vindas})
                #return HttpResponseRedirect('/principal/')
                
            except:
                return redirect_mensagem(1, 'index',request, 'Não foi possivel fazer o login.')
        else:
            return redirect_mensagem(1, 'index',request, 'Senha inválida!')
    except User.DoesNotExist:
        return redirect_mensagem(1, 'index',request, 'Usuário inválido!')
    

@csrf_exempt
def sair(request):
    logout(request)
    return HttpResponseRedirect('/')
'''
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def adm(request):
    if request.method == 'POST' and request.POST['username'] == 'admin':
        try:
            usuario_aux = User.objects.get(username=request.POST['username'])
            usuario = authenticate(username=usuario_aux.username,
                                   password=request.POST["password"])
            if usuario is not None:
                try:
                    login(request, usuario)
                    return HttpResponseRedirect('adm')
                except:
                    return redirect_mensagem(1, 'adm', request, 'Não foi possivel fazer o login.')
            else:
                return redirect_mensagem(1, 'adm', request, 'Senha inválida!')
        except User.DoesNotExist:
            return redirect_mensagem(1, 'adm', request, 'Usuário inválido!')
    else:
        return render(request, 'adm.html')
'''    
@csrf_exempt
@api_view(["GET"])
@login_required
@permission_classes((IsAuthenticated,))
def home(request):
    return render(request, 'index.html')

def redirect_mensagem(tipo=None, pagina=None, request=None, texto=None):
    if tipo == 0:
        messages.success(request, texto)
        return redirect(pagina)
    elif tipo == 1:
        messages.error(request, texto)
        return redirect(pagina)
    else:
        return redirect(pagina)


def verifica_login(request, pagina):
    if request.user.id is not None:
        return HttpResponseRedirect('/cadastro/')
    else:
        return render(request, pagina)


def notificar(assunto, remetente, destinatarios):
    try:
        mensagem_html = render_to_string('email.html')
        assunto = u"%s" % assunto
        remetente = u'%s' % remetente
        msg = EmailMultiAlternatives(assunto, mensagem_html, remetente, destinatarios)
        msg = msg.attach_alternative(mensagem_html, "text/html")
        msg.send()
    except Exception as exception:
        return exception
    
@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def populacao_view(request):
    # Obter os dados de população usando a função do populacao.py
    dados_ibge_2020 = obter_dados_ibge('2020')
    populacao_2020 = calcular_populacao_total(dados_ibge_2020)

    dados_ibge_2021 = obter_dados_ibge('2021')
    populacao_2021 = calcular_populacao_total(dados_ibge_2021)

    diferenca = calcular_diferenca(dados_ibge_2020, dados_ibge_2021)

 # Passar os dados para o template populacao.html
    context = {
        'populacao_2020': populacao_2020,
        'populacao_2021': populacao_2021,
        'diferenca': diferenca,
    }
    # Renderizar o template populacao.html com os dados
    return render(request, 'populacao.html', context)

def redirect_mensagem(tipo=None, pagina=None, request=None, texto=None):
    if tipo == 0:
        messages.success(request, texto)
        return redirect(pagina)
    elif tipo == 1:
        messages.error(request, texto)
        return redirect(pagina)
    else:
        return redirect(pagina)


def verifica_login(request, pagina):
    if request.user.id is not None:
        return HttpResponseRedirect('home')
    else:
        return render(request, pagina)


def notificar(assunto, remetente, destinatarios):
    try:
        mensagem_html = render_to_string('email.html')
        assunto = u"%s" % assunto
        remetente = u'%s' % remetente
        msg = EmailMultiAlternatives(assunto, mensagem_html, remetente, destinatarios)
        msg = msg.attach_alternative(mensagem_html, "text/html")
        msg.send()
    except Exception as exception:
        return exception
    return True

