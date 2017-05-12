# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from sistema.models import *
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, date

class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        somemodel_ct = ContentType.objects.get(app_label='auth', model='user')

        grupoadmin = Group(name = 'admin')
        grupoadmin.save()
        grupovendedor = Group(name = 'vendedor')
        grupovendedor.save()


        permadmin = Permission(name='Permissao admin', codename='is_admin',content_type=somemodel_ct)
        permadmin.save()
        permvendedor = Permission(name='Permissao vendedor', codename='is_vendedor',content_type=somemodel_ct)
        permvendedor.save()


        grupoadmin.permissions = [permadmin, permvendedor]
        grupovendedor.permissions = [permvendedor]

        user = User.objects.create_user('admin', 'admin@admin.com', 'admin')
        user.is_superuser = True
        user.is_staff = True
        user.group = [grupoadmin]
        user.save()

        user = User.objects.create_user('vendedor', 'vendedor@vendedor.com', 'vendedor')
        user.is_superuser = False
        user.is_staff = False
        user.group = [grupovendedor]
        user.save()


        def criar_faculdade(faculdade1):
            faculdade=Faculdade()
            faculdade.nome=faculdade1
            faculdade.save()
            return faculdade


        def criar_curso(curso1):
            curso=Curso()
            curso.nome=curso1
            curso.save()
            return curso

        faculdade1=criar_faculdade("Poli")
        faculdade2=criar_faculdade("FEA")
        faculdade3=criar_faculdade("IF")
        faculdade4=criar_faculdade("Ufscar")
        faculdade5=criar_faculdade("IME")

        curso1=criar_curso("Engenharia Elétrica")
        curso2=criar_curso("Engenharia Mecânica")
        curso3=criar_curso("Engenharia Civil")
        curso4=criar_curso("Engenharia Naval")

        def criar_participante(nome, sobrenome, faculdade, e_mail, telefone, curso, ano_ingresso):


            participante = Participante()
            participante.nome = nome
            participante.sobrenome=sobrenome
            participante.faculdade = faculdade
            participante.e_mail = e_mail
            participante.telefone = telefone
            participante.curso = curso
            participante.ano_ingresso = ano_ingresso
            participante.save()

            return participante




        def criar_atividade(nome, dia, horario, cap_participantes, pont_vendas, preco):
            atividade = Atividade()
            atividade.nome = nome
            atividade.dia = dia
            atividade.horario = horario
            atividade.cap_participantes = cap_participantes
            atividade.pont_vendas = pont_vendas
            atividade.preco = preco
            atividade.save()

            return atividade





        def criar_ponto_venda(nome):
            ponto = PontodeVenda()
            ponto.nome = nome
            ponto.save()
            return ponto

        def criar_vendedor(nome):
            vendedor = Vendedor()
            vendedor.nome = nome
            vendedor.save()
            return vendedor







        print 'Mockup feito com sucesso'
