from django.db import models
from django.contrib.auth.models import User

class Fichier(models.Model):
    nom = models.CharField(max_length=255)
    taille = models.IntegerField()
    type_fichier = models.CharField(max_length=50)
    emplacement = models.CharField(max_length=255)

class Transfert(models.Model):
    expéditeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='envois')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receptions')
    date = models.DateTimeField(auto_now_add=True)
    nombre_fichiers = models.IntegerField()
    taille_totale = models.IntegerField()

class HistoriqueTransfert(models.Model):
    transfert = models.ForeignKey(Transfert, on_delete=models.CASCADE, related_name='historique')
    fichier = models.ForeignKey(Fichier, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
