    # Create your views here.
# -*- coding: utf-8 -*-
import random
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.template import RequestContext, loader, Context
from sistema.models import *
from sistema.forms import *
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.views import password_change
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.core.validators import email_re
from django.forms.models import modelformset_factory
from django.core.mail import send_mail
from django.db.models import Q
import mimetypes, os
from os import path
import xlwt
def base(request):

	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	return render(request, 'base.html', locals())

################################## USUÁRIOS ###################################



def login_user(request):
	login_form = LoginForm()
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		usuario = request.POST.get("usuario")
		senha = request.POST.get("senha")
		user = authenticate(username=usuario, password=senha)
		if user is None:
			alerta = _(u'Usuário ou senha incorretos.')
			return render(request, "alerta.html", locals())
		if user is not None:
			login(request, user)
			return HttpResponseRedirect("/home/") #TODO colocar a url aqui
		else:
			return render (request, 'login.html', locals(), context_instance=RequestContext(request))
	else:
		return render (request, 'login.html', locals(), context_instance=RequestContext(request))
@login_required
def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/login/") #TODO colocar a url aqui


@login_required
def home(request):
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	return render(request, 'home.html', locals())

####################################PARTICIPANTE#############################################
@login_required
def participante_cadastrar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	participante_form = CriarParticipanteForm()
	if request.method == 'POST':
		participante_form = CriarParticipanteForm(request.POST)

		try:
			participante = participante_form.save(commit = False)
			participante.save()
			lista_atividades = Atividade.objects.all()
			# ponto_de_venda = PontodeVenda.objects.get(id = 1)
			# vendedor = Vendedor.objects.get(id = 1)
			#print(lista_atividades)
			tamanho_lista_atividades = len(lista_atividades)
			for atividade in lista_atividades:
				#foi retirado o reservado = False:
				compra = Compra(participante = participante, atividade = atividade, comprado = False, cortesia = False)
				compra.save()
			return HttpResponseRedirect('/lista_compra/%s' % str(participante.id))
		except:
			return HttpResponse("<script>alert('Preencha todos os campos!');javascript:history.back();</script>")



	return render(request,'participante_cadastrar.html', locals())


@login_required
def participante_dinamica(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	lista_participante = Participante.objects.filter().order_by("-nome_completo")
	return render(request, 'participante_dinamica.html', locals())

@login_required
def participante_dinamica2(request, id_faculdade):
	adm=False
	faculdade = Faculdade.objects.get(id= id_faculdade)
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	lista_participante = Participante.objects.filter(faculdade = faculdade).order_by("-nome_completo")
	return render(request, 'participante_dinamica2.html', locals())

@login_required
def participante_dinamica3(request, id_curso):
	adm=False
	curso = Curso.objects.get(id= id_curso)
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	lista_participante = Participante.objects.filter(curso = curso).order_by("-nome_completo")
	return render(request, 'participante_dinamica3.html', locals())

@login_required
def participante_dinamica4(request, id_local):
	adm=False
	local = PontodeVenda.objects.get(id = id_local)
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	compras = Compra.objects.filter(local = local)
	lista_participante = []
	participante0 = 0
	for compra in compras:
		participante1 = compra.participante
		if participante1 != participante0:
			lista_participante.append(participante1)
		participante0 = participante1
	return render(request, 'participante_dinamica4.html', locals())

@login_required
def participante_visualizar(request, id_participante):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	participante = Participante.objects.get(id = id_participante)
	lista_comprados = Compra.objects.filter(participante = participante).filter(comprado=True)
	lista_cortesia = Compra.objects.filter(participante = participante).filter(cortesia=True)
	#lista_reservados = Compra.objects.filter(participante = participante).filter(reservado=True)
	if participante.moleskine ==True:
		moleskine = True
	else:
		moleskine = False

	if participante.lancheira == True:
		lancheira = True
	else:
		lancheira = False
	if participante.aceita_divulgacao == True:
		divulgacao = True
	else:
		divulgacao = False
	if participante.ong == True:
		ong = True
	else:
		ong = False
	return render(request, 'participante_visualizar.html', locals())

@login_required
@permission_required('sistema.is_admin')
def participante_excluir(request, id_participante):

	participante = Participante.objects.get(id = id_participante)
	compras = Compra.objects.filter(participante = participante)
	for compra in compras:
		compra.delete()
	participante.delete()
	return HttpResponseRedirect('/participante_dinamica/')




@login_required
def participante_editar(request, id_participante):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	participante = Participante.objects.get(id = id_participante)
	participante_editar = CriarParticipanteForm(instance = participante)
	if request.method == 'POST' :
		participante_editar = CriarParticipanteForm(request.POST, instance = participante)

		try:
			participante = participante_editar.save(commit = False)
			participante.save()
			return HttpResponseRedirect('/participante_visualizar/%s' % str(participante.id))
		except:
			return HttpResponse("<script>alert('Preencha todos os campos!');javascript:history.back();</script>")



	return render (request, 'participante_editar.html', locals())




###############################################FACULDADE##########################################################
@login_required
def faculdade_cadastrar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	faculdade_form = CriarFaculdadeForm()
	if request.method == 'POST':
		faculdade_form = CriarFaculdadeForm(request.POST)
		if faculdade_form.is_valid():
			faculdade = faculdade_form.save(commit = False)
			faculdade.save()
			return HttpResponseRedirect('/faculdade_lista/')
	return render(request, 'faculdade_cadastrar.html',locals())

@login_required
def faculdade_visualizar(request, id_faculdade):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	faculdade = Faculdade.objects.get(id = id_faculdade)
	return render(request, 'faculdade_visualizar.html', locals())

@login_required
@permission_required('sistema.is_admin')
def faculdade_excluir(request, id_faculdade):
	faculdade = Faculdade.objects.get(id = id_faculdade)
	faculdade.delete()
	return HttpResponseRedirect('/faculdade_lista/')

@login_required
def faculdade_listar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	lista_faculdade = Faculdade.objects.filter()
	return render (request, 'faculdade_lista.html', locals())

@login_required
def faculdade_editar(request, id_faculdade):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	faculdade = Faculdade.objects.get(id = id_faculdade)
	faculdade_editar = CriarFaculdadeForm(instance = faculdade)
	if request.method == 'POST':
		faculdade_editar = CriarFaculdadeForm(request.POST, instance = faculdade)
		if faculdade_editar.is_valid():
			faculdade = faculdade_editar.save(commit = False)
			faculdade.save()
			return HttpResponseRedirect('/faculdade_lista/')
	return render (request, 'faculdade_editar.html', locals())


############################################## CURSO #######################################################

@login_required
def curso_cadastrar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	curso_form = CriarCursoForm()
	if request.method == 'POST':
		curso_form = CriarCursoForm(request.POST)
		if curso_form.is_valid():
			curso = curso_form.save(commit = False)
			curso.save()
			return HttpResponseRedirect('/curso_lista/')
	return render(request, 'curso_cadastrar.html',locals())

@login_required
def curso_visualizar(request, id_curso):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	curso = Curso.objects.get(id = id_curso)
	return render(request, 'curso_visualizar.html', locals())

@login_required
@permission_required('sistema.is_admin')
def curso_excluir(request, id_curso):
	curso = Curso.objects.get(id = id_curso)
	curso.delete()
	return HttpResponseRedirect('/curso_lista/')

@login_required
def curso_listar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	lista_curso = Curso.objects.filter()
	return render (request, 'curso_lista.html', locals())

@login_required
def curso_editar(request, id_curso):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	curso = Curso.objects.get(id = id_curso)
	curso_editar = CriarCursoForm(instance = curso)
	if request.method == 'POST':
		curso_editar = CriarCursoForm(request.POST, instance = curso)
		if curso_editar.is_valid():
			curso = curso_editar.save(commit = False)
			curso.save()
			return HttpResponseRedirect('/curso_lista/')
	return render (request, 'curso_editar.html', locals())

############################################## PONTO DE VENDA #######################################################
@login_required
@permission_required('sistema.is_admin')
def pontodevenda_cadastrar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	pontodevenda_form = CriarPontodeVendaForm()
	if request.method == 'POST':
		pontodevenda_form = CriarPontodeVendaForm(request.POST)
		if pontodevenda_form.is_valid():
			pontodevenda = pontodevenda_form.save(commit = False)
			pontodevenda.save()
			return HttpResponseRedirect('/pontodevenda_lista/')
	return render(request, 'pontodevenda_cadastrar.html',locals())

@login_required
@permission_required('sistema.is_admin')
def pontodevenda_excluir(request, id_pontodevenda):
	pontodevenda = PontodeVenda.objects.get(id = id_pontodevenda)
	pontodevenda.delete()
	return HttpResponseRedirect('/pontodevenda_lista/')

@login_required
@permission_required('sistema.is_admin')
def pontodevenda_listar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	lista_pontodevenda = PontodeVenda.objects.all().order_by('nome')
	return render (request, 'pontodevenda_lista.html', locals())

@login_required
@permission_required('sistema.is_admin')
def pontodevenda_editar(request, id_pontodevenda):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	pontodevenda = PontodeVenda.objects.get(id = id_pontodevenda)
	pontodevenda_editar = CriarPontodeVendaForm(instance = pontodevenda)
	if request.method == 'POST':
		pontodevenda_editar = CriarPontodeVendaForm(request.POST, instance = pontodevenda)
		if pontodevenda_editar.is_valid():
			pontodevenda = pontodevenda_editar.save(commit = False)
			pontodevenda.save()
			return HttpResponseRedirect('/pontodevenda_lista/')
	return render (request, 'pontodevenda_editar.html', locals())

############################################## VENDEDOR #######################################################
@login_required
@permission_required('sistema.is_admin')
def vendedor_cadastrar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	vendedor_form = CriarVendedorForm()
	if request.method == 'POST':
		vendedor_form = CriarVendedorForm(request.POST)
		if vendedor_form.is_valid():
			vendedor = vendedor_form.save(commit = False)
			try:
				vendedor.pontos = 0
				vendedor.save()
			except:
				return HttpResponse("<script>alert('Já existe um vendedor com este nome.');javascript:history.back();</script>")
			return HttpResponseRedirect('/vendedor_lista/')
	return render(request, 'vendedor_cadastrar.html',locals())

@login_required
@permission_required('sistema.is_admin')
def vendedor_excluir(request, id_vendedor):
	vendedor = Vendedor.objects.get(id = id_vendedor)
	vendedor.delete()
	return HttpResponseRedirect('/vendedor_lista/')

@login_required
@permission_required('sistema.is_admin')
def vendedor_listar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	vendedores = Vendedor.objects.all()
	for vendedor in vendedores:
		vendedor.pontos = 0
		vendas = Compra.objects.filter(comprado = True, vendedor = vendedor)
		cortesias = Compra.objects.filter(cortesia = True, vendedor = vendedor)
		for venda in vendas:
			vendedor.pontos+= venda.pontos
			vendedor.save()
		for cortesia in cortesias:
			vendedor.pontos+= cortesia.pontos
			vendedor.save()
	lista_vendedor = Vendedor.objects.all().order_by('-pontos')
	return render (request, 'vendedor_lista.html', locals())

@login_required
@permission_required('sistema.is_admin')
def vendedor_editar(request, id_vendedor):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	vendedor = Vendedor.objects.get(id = id_vendedor)
	vendedor_editar = CriarVendedorForm(instance = vendedor)
	if request.method == 'POST':
		vendedor_editar = CriarVendedorForm(request.POST, instance = vendedor)
		if vendedor_editar.is_valid():
			vendedor = vendedor_editar.save(commit = False)
			vendedor.save()
			return HttpResponseRedirect('/vendedor_lista/')
	return render (request, 'vendedor_editar.html', locals())

@login_required
@permission_required('sistema.is_admin')
def limpar_pontos(request):
	vendedores = Vendedor.objects.all()
	for vendedor in vendedores:
		compras = Compra.objects.filter(vendedor=vendedor)
		for compra in compras:
			compra.vendedor = None
			compra.save()
		vendedor.pontos = 0
		vendedor.save()

	return HttpResponseRedirect('/vendedor_lista/')

@login_required
def vendedor_clientes(request, id_vendedor):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	vendedor = Vendedor.objects.get(id=id_vendedor)
	vendas = Compra.objects.filter(vendedor= vendedor)
	clientes = []
	for venda in vendas:
		cliente1 = venda.participante
		if len(clientes) != 0:
			if cliente1 != cliente0:
				clientes.append(cliente1)
				cliente0 = cliente1
		else:
			clientes.append(cliente1)
			cliente0 = cliente1

	return render(request, 'vendedor_clientes.html', locals())




###################################### ATIVIDADE ########################################
@login_required
@permission_required('sistema.is_admin')
def atividade_cadastrar(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	criar_atividade = CriarAtividadeForm()
	if request.method == "POST":
		criar_atividade = CriarAtividadeForm(request.POST)
		if criar_atividade.is_valid():
			atividade = criar_atividade.save(commit = False)
			atividade.save()
			return HttpResponseRedirect('/atividade_lista/')
	return render(request, 'atividade_cadastrar.html', locals())

@login_required
def atividade_lista(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	atividade_lista = Atividade.objects.all()
	return render(request, 'atividade_lista.html', locals())

@login_required
@permission_required('sistema.is_admin')
def atividade_excluir(request, id_atividade):
	atividade = Atividade.objects.get(id = id_atividade)
	atividade.delete()
	return HttpResponseRedirect('/atividade_lista')

@login_required
@permission_required('sistema.is_admin')
def atividade_editar(request, id_atividade):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	atividade = Atividade.objects.get(id = id_atividade)
	atividade_editar = CriarAtividadeForm(instance = atividade)
	if request.method == 'POST' :
		atividade_editar = CriarAtividadeForm(request.POST, instance = atividade)
		if atividade_editar.is_valid():
			atividade = atividade_editar.save(commit = False)
			atividade.save()
		return HttpResponseRedirect('/atividade_lista')
	return render (request, 'atividade_editar.html', locals())

# @login_required
# def tabela_reservas(request):
# 	adm=False
# 	usuario = request.user
# 	if usuario.is_superuser ==True:
# 		adm= True
# 	atividades = Atividade.objects.all()
# 	atividade_lista = []
# 	for atividade in atividades:
# 		if atividade.reservas() > 0:
# 			atividade_lista.append(atividade)
# 	return render(request, 'tabela_reservas.html', locals())

# @login_required
# def lista_reserva(request, id_atividade):
# 	adm=False
# 	usuario = request.user
# 	if usuario.is_superuser ==True:
# 		adm= True
# 	atividade_selecionada = Atividade.objects.get(id = id_atividade)
# 	lista_reservas = Compra.objects.filter(reservado=True, atividade = atividade_selecionada)
# 	return render(request, 'lista_reserva.html', locals())

# @login_required
# def editar_reserva(request, id_atividade, id_participante):
# 	participante = Participante.objects.get(id = id_participante)
# 	atividade = Atividade.objects.get(id = id_atividade)
# 	compra= Compra.objects.get(atividade = atividade, participante=participante)
# 	compra.reservado=False
# 	compra.comprado=True
# 	compra.save()
# 	return HttpResponseRedirect('/lista_reserva/'+str(id_atividade))

# @login_required
# def excluir_reserva(request, id_atividade, id_participante):
# 	participante = Participante.objects.get(id = id_participante)
# 	atividade = Atividade.objects.get(id = id_atividade)
# 	compra= Compra.objects.get(atividade = atividade, participante=participante)
# 	compra.reservado=False
# 	compra.save()
# 	return HttpResponseRedirect('/lista_reserva/'+str(id_atividade))


# @login_required
# @permission_required('sistema.is_admin')
# def excluir_reservas(request):
# 	adm=False
# 	usuario = request.user
# 	if usuario.is_superuser ==True:
# 		adm= True
# 	reservas= Compra.objects.filter(reservado=True)
# 	for reserva in reservas:
# 		reserva.reservado = False
# 		reserva.save()
# 	return HttpResponseRedirect('/tabela_reservas/')

# @login_required
# @permission_required('sistema.is_admin')
# def excluir_reservas_atividade(request, id_atividade):
# 	adm=False
# 	usuario = request.user
# 	atividade = Atividade.objects.get(id = id_atividade)
# 	if usuario.is_superuser ==True:
# 		adm= True
# 	reservas= Compra.objects.filter(reservado=True, atividade= atividade)
# 	for reserva in reservas:
# 		reserva.reservado = False
# 		reserva.save()
# 	return HttpResponseRedirect('/lista_reserva/'+str(id_atividade))


@permission_required('sistema.is_admin')
@login_required
def lista_presenca(request, id_atividade):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	atividade_selecionada = Atividade.objects.get(id = id_atividade)
	lista_itens = Compra.objects.filter(Q(comprado=True, atividade = atividade_selecionada) | Q(cortesia = True, atividade = atividade_selecionada))
	compraram = lista_itens.count()

	lista_form = []
	post=False
	lista_presentes = []
	for compra in lista_itens:
		if compra.presente==True:
			lista_presentes.append([compra.participante, ListaPresencaForm(instance = compra, prefix=str(compra.participante.id))])
	presentes = len(lista_presentes)
	try:
		porcentagem_presenca = presentes*100/compraram
	except:
		porcentagem_presenca = 0
	for compra in lista_itens:
		lista_form.append([compra.participante, ListaPresencaForm(instance = compra, prefix=str(compra.participante.id))])
		if request.method == 'POST' :
			post=True
			lista_presenca_form = ListaPresencaForm(request.POST, instance = compra, prefix=str(compra.participante.id))
			lista_presenca = lista_presenca_form.save()
	if post:
		return HttpResponseRedirect('/lista_presenca/%s' % str(atividade_selecionada.id))
	return render (request, 'lista_presenca.html', locals())


@login_required
def lista_compra(request, id_participante):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	participante_selecionado = Participante.objects.get(id = id_participante)
	lista_itens = Compra.objects.filter(participante = participante_selecionado)
	lista_comprados = Compra.objects.filter(participante = participante_selecionado).filter(comprado=True)
	lista_cortesia = Compra.objects.filter(participante = participante_selecionado).filter(cortesia=True)
	#lista_reservados = Compra.objects.filter(participante = participante_selecionado).filter(reservado=True)
	lista_form = []
	lista_vendedor = [] #roda mais uma lista para nao alterar os pontos dos vendedores a cada nova compra
	valor = 0


	for compra in lista_itens:
		if compra.comprado == False and compra.cortesia == False:
			lista_vendedor.append(compra)


		lista_form.append([compra.atividade, CompraForm(instance = compra, prefix=str(compra.atividade.id))])

		if request.method == 'POST' :

			if compra.atividade.cap_atual() > 0:
				compra_form = CompraForm(request.POST, instance = compra, prefix=str(compra.atividade.id))
				lista_form = []
				for compra2 in lista_itens:
					lista_form.append([compra2.atividade, CompraForm(instance = compra2, prefix=str(compra2.atividade.id))])
				compra = compra_form.save()
				# foi retirado or (compra.comprado==True and compra.reservado==True) or (compra.reservado==True and compra.cortesia==True) :

				if (compra.comprado==True and compra.cortesia==True):
					compra.comprado=False
					#compra.reservado = False
					compra.cortesia = False
					compra.save()


					return HttpResponse("<script>alert('Existe mais de uma caixa selecionada em algum dos ingressos.');javascript:history.back();</script>")

			else:
				compra_form = CompraForm(request.POST, instance = compra, prefix=str(compra.atividade.id))
				lista_form = []
				for compra2 in lista_itens:
					lista_form.append([compra2.atividade, CompraForm(instance = compra2, prefix=str(compra2.atividade.id))])
				compra = compra_form.save()
				# foi retirado compra.reservado ==True
				if compra.comprado or compra.cortesia:
					compra.comprado = False
					#compra.reservado = False
					compra.cortesia = False
					compra.save()
					return HttpResponse("<script>alert('Atividade lotada!');javascript:history.back();</script>")

			if compra.comprado:
				valor = valor + compra.atividade.preco
	for nova_compra in lista_vendedor:
		if nova_compra.comprado or nova_compra.cortesia:
			nova_compra.pontos = nova_compra.atividade.pont_vendas
			nova_compra.save()



	return render (request, 'lista_compra.html', locals())



@login_required
@permission_required('sistema.is_admin')
def tabela_relatorios(request):
	adm=False
	usuario = request.user
	if usuario.is_superuser ==True:
		adm= True
	participantes = Participante.objects.all()
	cadastrados = Participante.objects.all().count()
	interessados_ong = Participante.objects.filter(ong=True).count()
	try:
		porcentagem_ong = interessados_ong*100/cadastrados
	except:
		porcentagem_ong = 0
	num_mailing = Participante.objects.filter(aceita_divulgacao=True).count()
	try:
		porcentagem_mailing = num_mailing*100/cadastrados
	except:
		porcentagem_mailing = 0
	tem_ingressos = 0
	moleskines = 0
	lancheiras = 0
	candidatos_lancheira = 0
	candidatos_excel = 0
	vendidos = 0
	num_cortesias = 0
	compareceram = 0
	for participante in participantes:
		if participante.moleskine:
			moleskines += 1
		if participante.lancheira:
			lancheiras += 1

		pagou = Compra.objects.filter(participante = participante, comprado =True).count()
		vendidos+=pagou
		ganhou = Compra.objects.filter(participante = participante, cortesia =True).count()
		num_cortesias+=ganhou
		num_atividades = pagou + ganhou
		if num_atividades > 4:
			tem_ingressos+=1
			candidatos_lancheira += 1
		elif num_atividades > 0:
			tem_ingressos+=1
		try:
			participou = Compra.objects.filter(presente=True, participante = participante).count()
			if participou > 2:
				compareceram +=1
				candidatos_excel+=1
			elif participou > 0:
				compareceram +=1
		except:
			pass
	ingressos = vendidos + num_cortesias
	lugares_ocupados = Compra.objects.filter(presente=True).count()
	try:
		abstencao_atividades = 100-((lugares_ocupados*100)/ingressos)
	except:
		abstencao_atividades = 0

	try:
		porcentagem_ingressos = 100*tem_ingressos/cadastrados
	except:
		porcentagem_ingressos = 0

	try:
		abstencao_participantes = 100-((compareceram*100)/tem_ingressos)
	except:
		abstencao_participantes = 0

	lista_comprados = Compra.objects.filter(comprado=True)
	#lista_reservados = Compra.objects.filter(reservado=True)
	lista_cortesias = Compra.objects.filter(cortesia=True)
	num_site = Compra.objects.filter(comprado=True, local__id = 3).count()
	lista_site = Compra.objects.filter(comprado=True, local__id = 3)
	#num_reservados = Compra.objects.filter(reservado=True).count()
	valor_total = 0
	valor_fisico = 0
	valor_online = 0
	previsao = 0
	valor_cortesias = 0
	for comprado in lista_site:
		valor_online+=comprado.atividade.preco
	for comprado in lista_comprados:
		valor_total+=comprado.atividade.preco
	valor_fisico = valor_total - valor_online
	valor_online = valor_online - num_site
	valor_total = valor_fisico + valor_online
	# for reservado in lista_reservados:
	# 	previsao+=reservado.atividade.preco
	for cortesia in lista_cortesias:
		valor_cortesias+=cortesia.atividade.preco

	return render(request, 'tabela_relatorios.html', locals())

# @login_required
# @permission_required('sistema.is_admin')
# def emails_reserva (request, id_atividade):
# 	atividade_selecionada = Atividade.objects.get(id = id_atividade)
# 	compras = Compra.objects.filter(reservado=True, atividade = atividade_selecionada)
# 	lista_emails = []

# 	for compra in compras:
# 		lista_emails.append(compra.participante.e_mail + "; ")

# 	workbook = xlwt.Workbook()
# 	worksheet = workbook.add_sheet(u'Cobrança de reserva')

# 	worksheet.write(0, 0, u'Emails')

# 	worksheet.write(1, 0, lista_emails)
# 	response = HttpResponse(mimetype='application/vnd.ms-excel')
# 	response['Content-Disposition'] = 'attachment; filename=reservas.xls'
# 	workbook.save(response)
# 	return response


@login_required
@permission_required('sistema.is_admin')
def lista_emails (request, id_atividade):
	atividade_selecionada = Atividade.objects.get(id = id_atividade)
	compras = Compra.objects.filter(comprado=True, atividade = atividade_selecionada)
	lista_emails = []

	for compra in compras:
		lista_emails.append(compra.participante.e_mail + "; ")

	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'Email de confirmação')

	worksheet.write(0, 0, u'Emails')

	worksheet.write(1, 0, lista_emails)
	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=emails.xls'
	workbook.save(response)
	return response

@login_required
@permission_required('sistema.is_admin')
def lista_excel (request):
	participantes = Participante.objects.all()
	lista_excel = []
	for participante in participantes:
		atividades = Compra.objects.filter(participante = participante, presente=True).count()
		if atividades >=3:
			lista_excel.append(participante)


	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'Candidatos ao curso de Excel')

	worksheet.write(0, 0, u'ID')
	worksheet.write(0, 1, u'Nome')
	worksheet.write(0, 2, u'Email')
	worksheet.write(0, 3, u'Telefone')
	worksheet.write(0, 4, u'Faculdade')
	worksheet.write(0, 5, u'Curso')
	worksheet.write(0, 6, u'Ano de Ingresso')

	i=1
	for participante in lista_excel:
		worksheet.write(i + 1, 0, i)
		worksheet.write(i + 1, 1, participante.nome_completo)
		worksheet.write(i + 1, 2, participante.e_mail)
		worksheet.write(i + 1, 3, participante.telefone)
		worksheet.write(i + 1, 4, participante.faculdade.nome)
		worksheet.write(i + 1, 5, participante.curso.nome)
		worksheet.write(i + 1, 6, participante.ano_ingresso)

		i=i+1

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Sorteio Excel.xls'
	workbook.save(response)
	return response

@login_required
@permission_required('sistema.is_admin')
def lista_ong (request):
	interessados = Participante.objects.filter(ong=True)
	lista_emails = []
	for participante in interessados:
		lista_emails.append(participante.e_mail + "; ")


	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'Email Ong')

	worksheet.write(0, 0, u'Interessados')

	worksheet.write(1, 0, lista_emails)

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Ong.xls'
	workbook.save(response)
	return response

@login_required
@permission_required('sistema.is_admin')
def lista_mailing (request):
	participantes = Participante.objects.filter(aceita_divulgacao=True)
	participantes2 = Participante.objects.filter(aceita_divulgacao = None)
	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'25ª SCE')

	worksheet.write(0, 0, u'ID')
	worksheet.write(0, 1, u'Nome')
	worksheet.write(0, 2, u'Email')
	worksheet.write(0, 3, u'Telefone')
	worksheet.write(0, 4, u'Faculdade')
	worksheet.write(0, 5, u'Curso')
	worksheet.write(0, 6, u'Ano de Ingresso')


	i=1
	for participante in participantes:

		worksheet.write(i + 1, 0, i)
		worksheet.write(i + 1, 1, participante.nome_completo)
		worksheet.write(i + 1, 2, participante.e_mail)
		worksheet.write(i + 1, 3, participante.telefone)
		worksheet.write(i + 1, 4, participante.faculdade.nome)
		worksheet.write(i + 1, 5, participante.curso.nome)
		worksheet.write(i + 1, 6, participante.ano_ingresso)
		i=i+1

	i=1
	for participante in participantes2:

		worksheet.write(i + 1, 0, i)
		worksheet.write(i + 1, 1, participante.nome_completo)
		worksheet.write(i + 1, 2, participante.e_mail)
		worksheet.write(i + 1, 3, participante.telefone)
		worksheet.write(i + 1, 4, participante.faculdade.nome)
		worksheet.write(i + 1, 5, participante.curso.nome)
		worksheet.write(i + 1, 6, participante.ano_ingresso)
		i=i+1

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Mailing List 25ª SCE.xls'
	workbook.save(response)
	return response


@login_required
@permission_required('sistema.is_admin')
def lista_brindes (request):
	lista_emails = []
	lista_emails2 = []
	participantes = Participante.objects.all()
	for participante in participantes:
		compras = Compra.objects.filter(comprado=True, participante= participante).count()
		if compras > 0:
			if participante.moleskine == False:
				lista_emails.append(participante.e_mail + "; ")
		if compras >= 5:
			if participante.lancheira == False:
				lista_emails2.append(participante.e_mail + "; ")

	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'Email Brindes')

	worksheet.write(0, 0, u'Participantes sem moleskine')

	worksheet.write(1, 0, lista_emails)

	worksheet.write(0, 1, u'Participantes sem lancheira')

	worksheet.write(1, 1, lista_emails2)


	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Pessoas sem brinde.xls'
	workbook.save(response)
	return response

@login_required
@permission_required('sistema.is_admin')
def relatorio_vendedores (request):

	vendedores = Vendedor.objects.all()

	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'Pontuação de Vendedores')

	worksheet.write(0, 0, u'Vendedores')
	i=0
	for vendedor in vendedores:
		worksheet.write(i+1, 0, vendedor.nome)
		worksheet.write(i+1, 1, vendedor.pontos)
		i=i+1

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Apoios.xls'
	workbook.save(response)
	return response

@login_required
@permission_required('sistema.is_admin')
def relatorio_geral (request):
	participantes = Participante.objects.all()
	num_participantes = Participante.objects.all().count()
	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'Participantes')

	worksheet.write(0, 0, u'ID')
	worksheet.write(0, 1, u'Nome')
	worksheet.write(0, 2, u'Email')
	worksheet.write(0, 3, u'Telefone')
	worksheet.write(0, 4, u'Faculdade')
	worksheet.write(0, 5, u'Curso')
	worksheet.write(0, 6, u'Ano de Ingresso')
	worksheet.write(0, 7, u'Aceita divulgação?')
	worksheet.write(0, 8, u'Quer participar da atividade com a ONG?')
	worksheet.write(0, 9, u'Atividades Compradas')
	worksheet.write(0, 10, u'Atividades Comparecidas')



	i=0
	for participante in participantes:
		if participante.aceita_divulgacao:
			divulgacao=u'Sim'
		else:
			divulgacao=u'Não'

		if participante.ong:
			ong=u'Sim'
		else:
			ong=u'Não'

		atividades_comparecidas = Compra.objects.filter(participante = participante, presente = True).count()
		atividades_compradas = Compra.objects.filter(participante = participante, comprado = True).count()

		worksheet.write(i + 1, 0, participante.id)
		worksheet.write(i + 1, 1, participante.nome_completo)
		worksheet.write(i + 1, 2, participante.e_mail)
		worksheet.write(i + 1, 3, participante.telefone)
		worksheet.write(i + 1, 4, participante.faculdade.nome)
		worksheet.write(i + 1, 5, participante.curso.nome)
		worksheet.write(i + 1, 6, participante.ano_ingresso)
		worksheet.write(i + 1, 7, divulgacao)
		worksheet.write(i + 1, 8, ong)
		worksheet.write(i + 1, 9, atividades_compradas)
		worksheet.write(i + 1, 10, atividades_comparecidas)

		i=i+1
########Ponto de Venda########
	ponto_lista = PontodeVenda.objects.all()
	worksheet2 = workbook.add_sheet(u'Pontos de Venda')

	worksheet2.write(0, 0, u'Ponto de Venda')
	worksheet2.write(0, 1, u'Número de Inscritos')
	worksheet2.write(0, 2, u'Ingressos Vendidos')
	i=0
	for local in ponto_lista:
		inscritos = 0
		ingressos_vendidos = Compra.objects.filter(comprado = True, local = local).count()
		for participante in participantes:

			comprou = Compra.objects.filter(comprado= True, local=local, participante = participante).count()
			if not comprou == 0:
				inscritos = inscritos + 1

		worksheet2.write(i + 1, 0, local.nome)
		worksheet2.write(i + 1, 1, inscritos)
		worksheet2.write(i + 1, 2, ingressos_vendidos)
		i=i+1

######### Atividades #######
	atividade_lista = Atividade.objects.all()


	worksheet3 = workbook.add_sheet(u'Atividades')

	worksheet3.write(0, 0, u'Atividade')
	worksheet3.write(0, 1, u'Dia')
	worksheet3.write(0, 2, u'Horário')
	worksheet3.write(0, 3, u'Preço')
	worksheet3.write(0, 4, u'Vagas')
	worksheet3.write(0, 5, u'Overbooking')
	worksheet3.write(0, 6, u'Número de Vendas')
	worksheet3.write(0, 7, u'Número de Participantes')
	worksheet3.write(0, 8, u'Valor arrecadado')
	worksheet3.write(0, 9, u'Abstenção')
	i=0

	for atividade in atividade_lista:
		lista_presentes=[]
		vendas=0
		compraram = Compra.objects.filter(comprado=True, atividade = atividade)
		for compra in compraram:
			vendas=vendas+1
			if compra.presente==True:
				lista_presentes.append([compra.participante, ListaPresencaForm(instance = compra, prefix=str(compra.participante.id))])
		presentes = len(lista_presentes)
		try:
			porcentagem_presenca = presentes*100/vendas
			abstencao = str(100-porcentagem_presenca) + u'%'
		except:
			porcentagem_presenca = 0
			abstencao = u'100%'
		valor = presentes*atividade.preco

		worksheet3.write(i + 1, 0, atividade.nome)
		worksheet3.write(i + 1, 1, atividade.dia)
		worksheet3.write(i + 1, 2, atividade.horario)
		worksheet3.write(i + 1, 3, atividade.preco)
		worksheet3.write(i + 1, 4, atividade.cap_participantes)
		worksheet3.write(i + 1, 5, atividade.overbooking)
		worksheet3.write(i + 1, 6, vendas)
		worksheet3.write(i + 1, 7, presentes)
		worksheet3.write(i + 1, 8, valor)
		worksheet3.write(i + 1, 9, abstencao)
		i=i+1

	######## Faculdades ########
	faculdades = Faculdade.objects.all()
	worksheet4 = workbook.add_sheet(u'Inscritos por faculdade')

	worksheet4.write(0, 0, u'Faculdade')
	worksheet4.write(0, 1, u'Número de Inscritos')
	worksheet4.write(0, 2, u'Presenças')
	i=0
	for faculdade in faculdades:
		inscritos = Participante.objects.filter(faculdade=faculdade).count()
		participantes_facul = Participante.objects.filter(faculdade=faculdade)
		presentes = 0
		for participante in participantes_facul:

			teste = Compra.objects.filter(participante = participante, presente = True).count()
			if teste > 0:
				presentes = presentes + 1

		worksheet4.write(i + 1, 0, faculdade.nome)
		worksheet4.write(i + 1, 1, inscritos)
		worksheet4.write(i + 1, 2, presentes)
		i=i+1

	######## Cursos ########
	cursos = Curso.objects.all()
	worksheet5 = workbook.add_sheet(u'Inscritos por curso')

	worksheet5.write(0, 0, u'Curso')
	worksheet5.write(0, 1, u'Número de Inscritos')
	i=0
	for curso in cursos:
		inscritos = Participante.objects.filter(curso=curso).count()
		worksheet5.write(i + 1, 0, curso.nome)
		worksheet5.write(i + 1, 1, inscritos)
		i=i+1

	######### Geral #######



	worksheet6 = workbook.add_sheet(u'Relatório Final')
	lista_presentes=[]
	valor_comprado = 0
	valor_doado = 0
	vendas = Compra.objects.filter(comprado=True).count()
	cortesias = Compra.objects.filter(cortesia=True).count()
	distribuidos = cortesias + vendas
	compras = Compra.objects.filter(comprado =True)
	doacoes = Compra.objects.filter(cortesia =True)
	for item in compras:
		valor_comprado += item.atividade.preco
	for item in doacoes:
		valor_doado += item.atividade.preco

	pagantes = 0
	doadores = 0
	clientes = 0
	presentes = 0
	for participante in participantes:

		pagou = Compra.objects.filter(participante = participante, comprado =True).count()
		doou = Compra.objects.filter(participante = participante, cortesia =True).count()
		presente = Compra.objects.filter(participante = participante, presente =True).count()
		if pagou > 0:
			pagantes+=1
		if doou > 0:
			doadores+=1
		if pagou or doou:
			clientes += 1
		if presente > 0:
			presentes+=1

	participacoes = Compra.objects.filter(presente=True).count()
	try:
		porcentagem_presenca = participacoes*100/vendas
		abstencao = str(100-porcentagem_presenca) + u'%'
	except:
		porcentagem_presenca = 0
		abstencao = u'100%'

	try:
		porcentagem_presenca = presentes*100/num_participantes
		abstencao2 = str(100-porcentagem_presenca) + u'%'
	except:
		porcentagem_presenca = 0
		abstencao2 = u'100%'



	worksheet6.write(0, 0, u'Lugares preenchidos')
	worksheet6.write(0, 1, u'Ingressos distribuídos')
	worksheet6.write(0, 2, u'Ingressos comprados')
	worksheet6.write(0, 3, u'Ingressos de cortesia')
	worksheet6.write(0, 4, u'Valor de vendas')
	worksheet6.write(0, 5, u'Valor de doações')
	worksheet6.write(0, 6, u'Abstenção (atividades)')
	worksheet6.write(0, 7, u'Cadastros')
	worksheet6.write(0, 8, u'Pegaram ingressos')
	worksheet6.write(0, 9, u'Pagantes')
	worksheet6.write(0, 10, u'Doadores')
	worksheet6.write(0, 11, u'Participantes')
	worksheet6.write(0, 12, u'Abstenção (participantes)')



	worksheet6.write(1, 0, participacoes)
	worksheet6.write(1, 1, distribuidos)
	worksheet6.write(1, 2, vendas)
	worksheet6.write(1, 3, cortesias)
	worksheet6.write(1, 4, valor_comprado)
	worksheet6.write(1, 5, valor_doado)
	worksheet6.write(1, 6, abstencao)
	worksheet6.write(1, 7, num_participantes)
	worksheet6.write(1, 8, clientes)
	worksheet6.write(1, 9, pagantes)
	worksheet6.write(1, 10, doadores)
	worksheet6.write(1, 11, presentes)
	worksheet6.write(1, 12, abstencao2)



	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Relatório Geral.xls'
	workbook.save(response)
	return response



@login_required
@permission_required('sistema.is_admin')
def relatorio_atividade (request, id_atividade):

	participantes = []
	compras = Compra.objects.filter(atividade=id_atividade, presente=True)
	for compra in compras:
		participantes.append(compra.participante)

	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'Participantes')

	worksheet.write(0, 0, u'ID')
	worksheet.write(0, 1, u'Nome')
	worksheet.write(0, 2, u'Email')
	worksheet.write(0, 3, u'Telefone')
	worksheet.write(0, 4, u'Faculdade')
	worksheet.write(0, 5, u'Curso')
	worksheet.write(0, 6, u'Ano de Ingresso')
	worksheet.write(0, 7, u'Aceita divulgação?')

	i=0
	for participante in participantes:
		if participante.aceita_divulgacao:
			divulgacao=u'Sim'
		else:
			divulgacao=u'Não'
		worksheet.write(i + 1, 0, participante.id)
		worksheet.write(i + 1, 1, participante.nome_completo)
		worksheet.write(i + 1, 2, participante.e_mail)
		worksheet.write(i + 1, 3, participante.telefone)
		worksheet.write(i + 1, 4, participante.faculdade.nome)
		worksheet.write(i + 1, 5, participante.curso.nome)
		worksheet.write(i + 1, 6, participante.ano_ingresso)
		worksheet.write(i + 1, 7, divulgacao)
		i=i+1

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Participantes.xls'
	workbook.save(response)
	return response

@login_required
@permission_required('sistema.is_admin')
def relatorio_atividade2 (request, id_atividade):

	participantes = []
	compras = Compra.objects.filter(atividade=id_atividade, comprado=True).order_by('participante__nome_completo')
	for compra in compras:
		participantes.append(compra.participante)

	cortesias = Compra.objects.filter(atividade=id_atividade, cortesia=True).order_by('participante__nome_completo')
	for cortesia in cortesias:
		participantes.append(cortesia.participante)

	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'Lista')

	worksheet.write(0, 0, u'#')
	worksheet.write(0, 1, u'Nome')
	worksheet.write(0, 2, u'Email')
	worksheet.write(0, 3, u'Telefone')
	worksheet.write(0, 4, u'Faculdade')
	worksheet.write(0, 5, u'Curso')
	worksheet.write(0, 6, u'Ano de Ingresso')
	worksheet.write(0, 7, u'Mailing')
	worksheet.write(0, 8, u'ONG')


	i=0
	for participante in participantes:
		if participante.aceita_divulgacao:
			divulgacao=u'Sim'
		else:
			divulgacao=u'Não'

		if participante.ong:
			ong=u'Sim'
		else:
			ong=u'Não'

		worksheet.write(i + 1, 0, i+1)
		worksheet.write(i + 1, 1, participante.nome_completo)
		worksheet.write(i + 1, 2, participante.e_mail)
		worksheet.write(i + 1, 3, participante.telefone)
		worksheet.write(i + 1, 4, participante.faculdade.nome)
		worksheet.write(i + 1, 5, participante.curso.nome)
		worksheet.write(i + 1, 6, participante.ano_ingresso)
		worksheet.write(i + 1, 7, divulgacao)
		worksheet.write(i + 1, 8, ong)
		i=i+1

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Lista.xls'
	workbook.save(response)
	return response

@login_required
@permission_required('sistema.is_admin')
def whatsapp (request, id_atividade):
	atividade = Atividade.objects.get(id=id_atividade)
	nome = atividade.nome
	participantes = []
	compras = Compra.objects.filter(atividade=id_atividade, comprado=True)
	for compra in compras:
		participantes.append(compra.participante)

	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet(u'Whatsapp')
	worksheet.write(0, 0, u'ID')
	worksheet.write(0, 1, u'Celular')
	i=0
	for participante in participantes:

		worksheet.write(i + 1, 0, nome + ' ' + str(i))
		worksheet.write(i + 1, 1, participante.telefone)

		i=i+1

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Whatsapp.xls'
	workbook.save(response)
	return response

