from django.db import models
from datetime import datetime

# Create your models here.

class Poste(models.Model):
    as_poste = models.CharField(max_length=6,verbose_name="ALIAS_Poste")
    nom_poste = models.CharField(max_length=62,verbose_name="Poste")
    somme = models.IntegerField()
    def __str__(self):
        return self.as_poste



class Personnel(models.Model):
    # nom de l'emplouyés
    name = models.CharField(max_length=64,verbose_name="Nom")
    # prénom de l'emplouyés
    prenom = models.CharField(max_length=64,verbose_name="Prénom")
    # email de l'emplouyés
    email = models.EmailField(unique=True,verbose_name="Email")
    #horaire_m = models.IntegerField(null=True,verbose_name="Horaire menseule")
    # poste auccupé par l'emplouyés
    poste = models.ForeignKey(Poste,on_delete=models.CASCADE,verbose_name="Poste")
    # nom de l'emplouyés
    gender = models.CharField(max_length=100, choices=[('Masculin','Masculin'),('Feminin','Feminin')])
    class Meta:
        verbose_name ="Personnel"
        verbose_name_plural ="Personnels"
    def __str__(self):
        return self.name

class Horaire(models.Model):
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE,verbose_name="Horaire")

    def calculate_duration(self):
        arrival = datetime.combine(datetime.today(), self.arrival_time)
        departure = datetime.combine(datetime.today(), self.departure_time)

        duration = departure - arrival

        return duration
   
    def __str__(self):
        return self.pk

class Attendance(models.Model):
    personnel_a = models.ForeignKey(Personnel,on_delete=models.CASCADE)
    horaire_a = models.ForeignKey(Horaire,on_delete=models.CASCADE)