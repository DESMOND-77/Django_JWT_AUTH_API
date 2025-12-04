from django.db import models

class Etablissement(models.Model):
    # id = models.BigAutoField()
    id = models.CharField(primary_key=True,unique=True, max_length=50)
    name = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=7, blank=True, null=True)

   