from django.db import models


# Create your models here.

class Poste(models.Model):
    id_poste = models.CharField(max_length=6,verbose_name="ID_Poste")
    nom_poste = models.CharField(max_length=62,verbose_name="Poste")
    somme = models.IntegerField()
    def __str__(self):
        return self.id_poste


class Horaire(models.Model):
    jour = models.CharField(max_length=10,verbose_name="JOUR")
    mois = models.CharField(max_length=12,verbose_name="MOIS")
    nbre_d = models.IntegerField(verbose_name="Numero")
    heure_arrive = models.TimeField(auto_now=True ,max_length=12,verbose_name="Time_IN",null=True)
    heure_sorti = models.TimeField(auto_now=True ,max_length=12,verbose_name="Time_OUT",null=True)
    duree = models.IntegerField(verbose_name="Heure_effectue")
    def __str__(self):
        return self.jour


class Personnel(models.Model):
    # nom de l'emplouyés
    name = models.CharField(max_length=64,verbose_name="Nom")
    # prénom de l'emplouyés
    prenom = models.CharField(max_length=64,verbose_name="Prénom")
    # email de l'emplouyés
    email = models.EmailField(unique=True,verbose_name="Email")
    horaire_m = models.IntegerField(null=True,verbose_name="Horaire menseule")
    # poste auccupé par l'emplouyés
    poste = models.ForeignKey(Poste,on_delete=models.PROTECT,verbose_name="Poste")
    # nom de l'emplouyés
    gender = models.CharField(max_length=100, choices=[('Male','Male'),('Female','Female')])
    class Meta:
        verbose_name ="Personnel"
        verbose_name_plural ="Personnels"
    def __str__(self):
        return self.name


