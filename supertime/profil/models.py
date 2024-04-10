from django.db import models
from datetime import datetime,date

# Create your models here.

class Poste(models.Model):
    as_poste = models.CharField(max_length=6,verbose_name="ALIAS_Poste")
    nom_poste = models.CharField(max_length=62,verbose_name="Poste")
    somme = models.IntegerField(default='2500')
    heure_debut= models.TimeField(default='08:00',null=True)
    heure_fin = models.TimeField(default='08:00',null=True)
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
    gender = models.CharField(default='Masculin',max_length=100, choices=[('Masculin','Masculin'),('Feminin','Feminin')],verbose_name="Genre")
    heure_fixe = models.IntegerField(default='100',null=True)# n
    salary = models.FloatField(default='0',null=True) # n
    is_present = models.CharField(max_length=24,choices=[('Present','Present'),('Absent','Absent')])

    class Meta:
        verbose_name ="Personnel"
        verbose_name_plural ="Personnels"
    def __str__(self):
        return self.name

class Horaire(models.Model):
    date_d = models.DateField(null=True) # n
    arrival_time = models.TimeField(default='08:30',null=True)
    departure_time = models.TimeField(default='17:40',null=True)
    personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE,verbose_name="Personnel")


    def calculate_duration(self):
        arrival = datetime.combine(datetime.today(), self.arrival_time)
        departure = datetime.combine(datetime.today(), self.departure_time)

        duration = departure - arrival

        return duration
   
    def retard(self):
        h_arrival = datetime.combine(datetime.today(), self.arrival_time)
        h_arrival_fixe = datetime.combine(datetime.today(), self.personnel.poste.heure_debut)
        # if h_arrival < h_arrival_fixe:
        #    h_resultant_r= h_arrival_fixe - h_arrival
        # else:
        #      h_resultant_r= h_arrival_fixe - h_arrival
        if h_arrival > h_arrival_fixe:
           h_resultant_r=    h_arrival-h_arrival_fixe
        else:
            h_d = "00:00"
            h_resultant_r = datetime.strptime(h_d,"%H:%M").time()


        return h_resultant_r
    def date_days(self):
        d=date.today().strftime('%m-%Y')
        return d
    
    def __str__(self):
        return self.pk
    

class Attendance(models.Model):
    personnel_a = models.ForeignKey(Personnel,on_delete=models.CASCADE)
    horaire_a = models.ForeignKey(Horaire,on_delete=models.CASCADE)