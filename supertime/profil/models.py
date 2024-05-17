from django.db import models
from datetime import datetime,date
from django.contrib.auth.models import User

# Create your models here.

class Poste(models.Model):
    as_poste = models.CharField(max_length=6,verbose_name="ALIAS_Poste",null=True)
    nom_poste = models.CharField(max_length=62,verbose_name="Poste",null=True)
    somme = models.IntegerField(default='2500',null=True)
    heure_debut= models.TimeField(default='08:00',null=True)
    heure_fin = models.TimeField(default='18:00',null=True)
    tolerance_time=models.TimeField(default='08:30',null=True)
    def __str__(self):
        return self.as_poste



class Personnel(models.Model):
    # nom de l'emplouyés
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64,verbose_name="Nom",null=True)
    # prénom de l'emplouyés
    prenom = models.CharField(max_length=64,verbose_name="Prénom",null=True)
    # email de l'emplouyés
    email = models.EmailField(unique=True,verbose_name="Email",null=True)
    #horaire_m = models.IntegerField(null=True,verbose_name="Horaire menseule")
    # poste auccupé par l'emplouyés
    poste = models.ForeignKey(Poste,on_delete=models.CASCADE,verbose_name="Poste")
    # nom de l'emplouyés
    gender = models.CharField(default='Masculin',max_length=100, choices=[('Masculin','Masculin'),('Feminin','Feminin')],verbose_name="Genre")
    heure_fixe = models.IntegerField(default='100',null=True)# n
    salary = models.FloatField(default='0',null=True) # n
    
    class Meta:
        verbose_name ="Personnel"
        verbose_name_plural ="Personnels"
    def __str__(self):
        return self.name

class Horaire(models.Model):
    date_d = models.DateTimeField(null=True) # n
    arrival_time = models.DateTimeField(null=True)
    departure_time = models.DateTimeField(null=True)
    personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE,verbose_name="Personnel")
    status = models.CharField(max_length=65,null=True, blank=True)
    # punch = models.CharField(max_length=65,null=True, blank=True)
    # id_att=models.IntegerField(null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def calculate_duration(self):
        check_in_time = datetime.combine(datetime.today(), self.arrival_time)
        check_out_time = datetime.combine(datetime.today(), self.departure_time)
        start_time=datetime.combine(datetime.today(),self.personnel.poste.heure_debut)
        end_time=datetime.combine(datetime.today(),self.personnel.poste.heure_fin)
        tolerance_time=datetime.combine(datetime.today(),self.personnel.poste.tolerance_time)
        if check_in_time < tolerance_time:
            if check_out_time > end_time:
                real_time = end_time - check_in_time
            elif check_in_time < start_time:
                real_time = check_out_time - start_time
            else:
                real_time = check_out_time - check_in_time
        else:

            real_time =datetime.strptime("00:00","%H:%M").time()
        #duration = check_in_time - check_out_time

        return real_time
   
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
    # horaire_a = models.ForeignKey(Horaire,on_delete=models.CASCADE)
    id_att=models.IntegerField(unique=True,null=True)
    date = models.DateTimeField(null=True)
    heure_punch = models.DateTimeField(null=True, )
    status = models.CharField(max_length=65,null=True, )
    punch = models.CharField(max_length=65,null=True, )
    # Autres champs pour les informations de présence

    def __str__(self):
        return f"{self.personnel_a.name} - {self.date}"


class Zklecteur(models.Model):
    ip_adresse = models.CharField(max_length=32)
    n_port = models.IntegerField(default='4370')