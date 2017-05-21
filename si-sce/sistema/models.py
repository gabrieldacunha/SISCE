from django.db import models
import os
import datetime
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver



tipos_de_compras = (
	('normal', 'Normal'),
	('cortesia', 'Cortesia'),
	('reserva', 'Reserva'),
	('----','----')
)

dia = (
	('Segunda-Feira', "Segunda-Feira"),
	('Terca-Feira', "Terca-Feira"),
	('Quarta-Feira', "Quarta-Feira"),
	('Quinta-Feira', "Quinta-Feira"),
	('Sexta-Feira', "Sexta-Feira"),

)
class Usuario(models.Model):
	nome = models.CharField("Usuario", max_length=64)
	usuario = models.OneToOneField(User, related_name = 'usuario')

	def __unicode__(self):
		return self.nome

class Faculdade(models.Model):
	nome = models.CharField("Faculdade", max_length=64)
	class Meta:
		ordering = ["nome"]
	def __unicode__(self):
		return self.nome

	def participantes(self):
		participantes = Participante.objects.filter(faculdade__nome = self.nome).count()

		return	participantes

class Curso(models.Model):
	nome = models.CharField("Curso", max_length=64)
	class Meta:
		ordering = ["nome"]
	def __unicode__(self):
		return self.nome

	def participantes(self):
		participantes = Participante.objects.filter(curso__nome = self.nome).count()

		return	participantes

class Participante(models.Model):
	nome_completo = models.CharField("Nome completo", max_length=256)
	cpf = models.CharField("CPF", max_length=16)
	faculdade = models.ForeignKey(Faculdade)
	curso = models.ForeignKey(Curso)
	ano_ingresso = models.IntegerField("Ano de ingresso")
	e_mail = models.EmailField("E-mail")
	telefone = models.CharField("Telefone", max_length=16)
	moleskine = models.NullBooleanField()
	lancheira = models.NullBooleanField()
	aceita_divulgacao = models.NullBooleanField()
	ong = models.NullBooleanField()
	def __unicode__(self):
		return self.nome_completo

	def atividades(self):
		compradas = Compra.objects.filter(participante__nome_completo = self.nome_completo, comprado=True).count()
		cortesia = Compra.objects.filter(participante__nome_completo = self.nome_completo, cortesia=True).count()


		return	compradas + cortesia
	def presencas(self):
		presencas = Compra.objects.filter(participante__nome_completo = self.nome_completo, presente=True).count()
		return presencas


class Atividade(models.Model):
	nome = models.CharField("Nome", max_length=64)
	dia = models.CharField("Dia", choices = dia, max_length = 64)
	horario = models.CharField("Horario", max_length=64)
	# descricao = models.CharField("Descricao",max_length=64)
	cap_participantes = models.IntegerField("Capacidade de Participantes")
	overbooking = models.IntegerField("Overbooking", null=True, blank = True)
	cap_atual = models.IntegerField("Capacidade Atual")
	pont_vendas = models.IntegerField("Pontuacao de Vendas")
	preco = models.IntegerField("Preco")

	def __unicode__(self):
		return self.nome

	def cap_atual(self):
		compradas = Compra.objects.filter(atividade__nome=self.nome, comprado=True).count()
		# reservadas = Compra.objects.filter(atividade__nome=self.nome, reservado=True).count()
		cortesias = Compra.objects.filter(atividade__nome=self.nome, cortesia=True).count()
		cap_inicial = self.cap_participantes
		overbooking = self.overbooking
		cap_atual = cap_inicial + overbooking - cortesias - compradas

		return	cap_atual

	# def reservas(self):
	# 	reservas = Compra.objects.filter(atividade__nome=self.nome, reservado=True).count()

	# 	return reservas

	def vendas(self):
		vendidos = Compra.objects.filter(atividade__nome=self.nome, comprado=True).count()
		cortesia = Compra.objects.filter(atividade__nome=self.nome, cortesia=True).count()
		vendas = vendidos + cortesia
		return vendas

class Email(models.Model):
	corpo = models.CharField("Corpo", max_length=512)
	assunto = models.CharField("Assunto", max_length=64)

	def __unicode__(self):
		return self.nome

class Vendedor(models.Model):
	nome = models.CharField("Nome", max_length=64)
	pontos = models.IntegerField("Pontos", null=True, blank=True)
	class Meta:
		ordering = ["nome"]
	def __unicode__(self):
		return self.nome


class PontodeVenda(models.Model):
	nome = models.CharField("Local de Venda", max_length=64)
	class Meta:
		ordering = ["nome"]
	def __unicode__(self):
		return self.nome

class Compra(models.Model):
	participante = models.ForeignKey(Participante)
	atividade = models.ForeignKey(Atividade)
	local = models.ForeignKey(PontodeVenda, null=True, blank = True)
	vendedor = models.ForeignKey(Vendedor, null=True, blank = True)
	preco_pagar = models.IntegerField("Preco", null=True, blank=True)
	presente = models.BooleanField(default = False)
	comprado = models.BooleanField(default = False)
	#reservado = models.BooleanField(default = False)
	cortesia = models.BooleanField(default = False)
	pontos = models.IntegerField("Pontos", null=True, blank=True)


