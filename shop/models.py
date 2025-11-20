from django.db import models
from django.utils import timezone
from user.models import Client
#table categorie
class Categorie(models.Model):
     nom = models.CharField(max_length=40)

class Catalogue(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, max_length=100, default="Non classé")
    nom = models.CharField(max_length=200)
    description = models.CharField(max_length=2500)
    date_creation = models.DateTimeField(default= timezone.now)
    statut = models.enums

#mode de paiement
class ModePaiement(models.TextChoices):
      ORANGE_MONEY = "OM","ORANGE_MONEY"
      MOBILE_MONEY =  "MOMO", "MOBILE_MONEY"
      CARTE_BANCAIRE = "CB", "CARTE_BANCAIRE"
      PAIEMENT_APRES_LIVRAISON = "PAL", "PAIEMENT_APRES_LIVRAISON"

#retrait
class Retrait(models.Model):
     montant_total = models.DecimalField(max_digits=10, decimal_places=4)
#setails facture 
class Detail_facture(models.Model):
     quantite = models.IntegerField()
     prix_unitaire = models.DecimalField(max_digits=10, decimal_places=4)

#statut facture
class Statut_facture(models.TextChoices):
     PAYE = "P", "PAYE"
     EN_ATTENTE = "EA", "EN_ATTENTE"
     ANNULE = "A", "ANNULE"
class Facture(models.Model):
     client = models.ForeignKey(Client, on_delete=models.CASCADE)
     date_facture = models.DateTimeField(default=timezone.now)
     montant_total = models.DecimalField(max_digits=65, decimal_places=4)
     mode_paiement =models.CharField(max_length=10, choices=ModePaiement.choices,
                                     default=ModePaiement.ORANGE_MONEY,
     )
     statut = models.CharField(max_length=10, choices=Statut_facture.choices, default=Statut_facture.EN_ATTENTE,          
     )
     adresse_livraison = models.CharField(max_length=250)
     retrait = models.ForeignKey(Retrait, on_delete=models.CASCADE)
     detail_facture = models.ForeignKey(Detail_facture, on_delete=models.CASCADE)

#statut article
class Statut_article(models.TextChoices):
    EN_VENTE = "EN", "EN_VENTE"
    DEjA_VENDU = "DV", "DEJA_VENDU"

class Article(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE)
    nom = models.CharField(max_length=250)
    description = models.TextField()
    prix = models.IntegerField()
    quantite = models.IntegerField()
    actif = models.CharField(
                              max_length=10, 
                              choices = Statut_article.choices, 
                              default = Statut_article.EN_VENTE,
    )
    image = models.ImageField(upload_to="articles/", blank=True, null=True)
    def _str_(self):
        return self.nom


    