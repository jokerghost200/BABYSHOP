from django.db import models

class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=250)
    tel = models.CharField(max_length=15, default='000000000000000')
    email = models.CharField(max_length=255)
    adresse = models.CharField(max_length=50)
    ville = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    #parametre 
    langue = models.CharField(max_length=10, default='fr')
    notif_active = models.BooleanField(default=True)
    theme_sombre = models.BooleanField(default=False)
    alertes_email = models.BooleanField(default=True)
    maj_auto = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=True)
    partage_donnees = models.BooleanField(default=False)
    localisation = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.nom} - {self.email}"


