# Embedded file name: C:\Users\Gabriel\Documents\si_sce2\sistema\forms.py
import os, sys
from sistema.models import *
from django import forms
from django.contrib.localflavor.br.forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm, TextInput, Select
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory

# class LogarPontodeVendaForm(forms.ModelForm):

#     class Meta:
#         model = Usuario
#         fields = ['local']

class CriarParticipanteForm(forms.ModelForm):

    class Meta:
        model = Participante


class CriarAtividadeForm(forms.ModelForm):

    class Meta:
        model = Atividade


class CriarFaculdadeForm(forms.ModelForm):

    class Meta:
        model = Faculdade

class CriarCursoForm(forms.ModelForm):

    class Meta:
        model = Curso

class CriarPontodeVendaForm(forms.ModelForm):

    class Meta:
        model = PontodeVenda

class CriarVendedorForm(forms.ModelForm):

    class Meta:
        model = Vendedor
        fields = ['nome']


class LoginForm(forms.Form):
    usuario = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'text'}))
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'text'}))


class ListaPresencaForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['presente']


class CompraForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['comprado',
         'cortesia',
         'local',
         'vendedor']



class EmailForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = ['assunto', 'corpo']
