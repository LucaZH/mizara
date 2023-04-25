from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Fichier)
admin.site.register(HistoriqueTransfert)
admin.site.register(Transfert)