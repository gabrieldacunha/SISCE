import django
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib import admin
from sistema import views
import os
#from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^login/$', views.login_fazer),
    url(r'^si_sce2/static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(os.getcwd(),'static') }),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^base/$', views.base),
    url(r'^login/$', views.login_user),
    url(r'^$', views.home),
    url(r'^logout/$', views.logout_user),
    url(r'^home/$', views.home),

    #Atividade
    url(r'^atividade_cadastrar/$', views.atividade_cadastrar),
    url(r'^atividade_lista/$', views.atividade_lista),
    url(r'^atividade_editar/(?P<id_atividade>[0-9]+)/$', views.atividade_editar),
    url(r'^atividade_excluir/(?P<id_atividade>[0-9]+)/$', views.atividade_excluir),
    url(r'^lista_presenca/(?P<id_atividade>[0-9]+)/$', views.lista_presenca),
    # url(r'^tabela_reservas/$', views.tabela_reservas),
    # url(r'^lista_reserva/(?P<id_atividade>[0-9]+)/$', views.lista_reserva),
    # url(r'^editar_reserva/(?P<id_atividade>[0-9]+)/(?P<id_participante>[0-9]+)/$', views.editar_reserva),
    # url(r'^excluir_reserva/(?P<id_atividade>[0-9]+)/(?P<id_participante>[0-9]+)/$', views.excluir_reserva),
    # url(r'^excluir_reservas/$', views.excluir_reservas),
    # url(r'^excluir_reservas_atividade/(?P<id_atividade>[0-9]+)/$', views.excluir_reservas_atividade),
    url(r'^lista_emails/(?P<id_atividade>[0-9]+)/$', views.lista_emails),
    url(r'^pontodevenda_cadastrar/$', views.pontodevenda_cadastrar),
    url(r'^pontodevenda_excluir/(?P<id_pontodevenda>[0-9]+)/$', views.pontodevenda_excluir),
    url(r'^pontodevenda_lista/$', views.pontodevenda_listar),
    url(r'^pontodevenda_editar/(?P<id_pontodevenda>[0-9]+)/$', views.pontodevenda_editar),
    #url(r'^emails_reserva/(?P<id_atividade>[0-9]+)/$', views.emails_reserva),
    url(r'^participante_dinamica4/(?P<id_local>[0-9]+)/$', views.participante_dinamica4),

    #Participante
    url(r'^participante_cadastrar/$', views.participante_cadastrar),
    url(r'^participante_visualizar/(?P<id_participante>[0-9]+)/$', views.participante_visualizar),
    url(r'^participante_excluir/(?P<id_participante>[0-9]+)/$', views.participante_excluir),
    url(r'^participante_editar/(?P<id_participante>[0-9]+)/$', views.participante_editar),
    url(r'^participante_dinamica/$', views.participante_dinamica),


    #Faculdade
    url(r'^faculdade_cadastrar/$', views.faculdade_cadastrar),
    url(r'^faculdade_visualizar/(?P<id_faculdade>[0-9]+)/$',views.faculdade_visualizar),
    url(r'^faculdade_excluir/(?P<id_faculdade>[0-9]+)/$', views.faculdade_excluir),
    url(r'^faculdade_lista/$', views.faculdade_listar),
    url(r'^faculdade_editar/(?P<id_faculdade>[0-9]+)/$', views.faculdade_editar),
    url(r'^curso_cadastrar/$', views.curso_cadastrar),
    url(r'^curso_visualizar/(?P<id_curso>[0-9]+)/$',views.curso_visualizar),
    url(r'^curso_excluir/(?P<id_curso>[0-9]+)/$', views.curso_excluir),
    url(r'^curso_lista/$', views.curso_listar),
    url(r'^curso_editar/(?P<id_curso>[0-9]+)/$', views.curso_editar),
    url(r'^participante_dinamica2/(?P<id_faculdade>[0-9]+)/$', views.participante_dinamica2),
    url(r'^participante_dinamica3/(?P<id_curso>[0-9]+)/$', views.participante_dinamica3),

    #Vendedor
    url(r'^vendedor_cadastrar/$', views.vendedor_cadastrar),
    url(r'^vendedor_excluir/(?P<id_vendedor>[0-9]+)/$', views.vendedor_excluir),
    url(r'^vendedor_lista/$', views.vendedor_listar),
    url(r'^limpar_pontos/$', views.limpar_pontos),
    url(r'^vendedor_editar/(?P<id_vendedor>[0-9]+)/$', views.vendedor_editar),
    url(r'^vendedor_clientes/(?P<id_vendedor>[0-9]+)/$', views.vendedor_clientes),


    #Compra
    url(r'^lista_compra/(?P<id_participante>[0-9]+)/$', views.lista_compra),

    #Relatorio
    url(r'^tabela_relatorios/$', views.tabela_relatorios),
    url(r'^relatorio_geral/$', views.relatorio_geral),
    url(r'^relatorio_atividade/(?P<id_atividade>[0-9]+)/$', views.relatorio_atividade),
    url(r'^relatorio_atividade2/(?P<id_atividade>[0-9]+)/$', views.relatorio_atividade2),
    url(r'^whatsapp/(?P<id_atividade>[0-9]+)/$', views.whatsapp),
    url(r'^lista_excel/$', views.lista_excel),
    url(r'^lista_ong/$', views.lista_ong),
    url(r'^lista_mailing/$', views.lista_mailing),
    url(r'^lista_brindes/$', views.lista_brindes),
    url(r'^relatorio_vendedores/$', views.relatorio_vendedores),
)

