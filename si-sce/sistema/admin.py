from django.contrib import admin
from sistema.models import Participante
from sistema.models import Atividade
from sistema.models import Faculdade
from sistema.models import Vendedor
from sistema.models import PontodeVenda
from sistema.models import Compra

admin.site.register(Participante)
admin.site.register(Atividade)
admin.site.register(Faculdade)
admin.site.register(Vendedor)
admin.site.register(PontodeVenda)
admin.site.register(Compra)
# Register your models here.
