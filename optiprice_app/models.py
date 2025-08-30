from django.db import models

# Create your models here.

class User (models.Model):
    nom = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
class Recherche(models.Model):
    mot_cle = models.CharField(max_length=255)
    categorie = models.CharField(max_length=255)
    nbre_produits = models.PositiveIntegerField(default=10)
    date_recherche = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.mot_cle} ({self.nbre_produits})"