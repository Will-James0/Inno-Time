from django.db import models
from datetime import datetime,date
import time
from django.contrib.auth.models import User
import pytz

# Create your models here.

class Poste(models.Model):
    as_poste = models.CharField(max_length=60,verbose_name="ALIAS_Poste",null=True)
    nom_poste = models.CharField(max_length=62,verbose_name="Poste",null=True)
    somme = models.FloatField(null=True)
    heure_debut= models.TimeField(null=True)
    heure_fin = models.TimeField(null=True)
    tolerance_time=models.TimeField( null=True)
    time_work = models.IntegerField(null = True)
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
    gender = models.CharField(default='Masculin',max_length=100, choices=[('Masculin','Masculin'),('Feminin','Feminin')],verbose_name="Genre", null=True)
    heure_fixe = models.IntegerField(default='100',null=True)# n
    salary = models.FloatField(default='0',null=True) # n
    time_a = models.TimeField(null = True)
    tolerance_time=models.TimeField(null=True)
    time_s = models.TimeField(null=True)
    photo = models.ImageField(upload_to='photo_user/', blank=True, null=True)
    
    class Meta:
        verbose_name ="Personnel"
        verbose_name_plural ="Personnels"
    def __str__(self):
        return self.name
    def get_self(self):
        return Personnel.objects.get(user = self.user)

class Horaire(models.Model):
    date_d = models.DateTimeField(null=True) # n
    arrival_time = models.DateTimeField(null=True)
    departure_time = models.DateTimeField(null=True)
    personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE,verbose_name="Personnel")
    status = models.CharField(max_length=65,null=True, blank=True)
    statute = models.CharField(max_length=65, null= True)
    punch = models.CharField(max_length=65,null=True, blank=True)
    id_att=models.IntegerField(null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def calculate_duration(self):
        timezone = pytz.timezone('Africa/Douala')  # Par exemple, Africa/Douala
        check_in_time = self.arrival_time
        check_out_time = self.departure_time

        # Si check_out_time est None, définissez la durée à 00:00:00
        if check_out_time is None:
            return datetime.strptime("00:00:00", "%H:%M:%S").time()

        start_time = datetime.combine(check_in_time.date(), self.personnel.poste.heure_debut).replace(tzinfo=timezone)
        end_time = datetime.combine(check_out_time.date(), self.personnel.poste.heure_fin).replace(tzinfo=timezone)
        tolerance_time = datetime.combine(check_in_time.date(), self.personnel.tolerance_time)

        # Ajoutez le fuseau horaire à l'objet datetime
        tolerance_datetime = tolerance_time.replace(tzinfo=timezone)
        if check_in_time < tolerance_datetime:
            if check_out_time > end_time:
                real_time = end_time - check_in_time
            elif check_in_time < start_time:
                real_time = check_out_time - start_time
            else:
                real_time = check_out_time - check_in_time
        else:
            real_time = datetime.strptime("00:00", "%H:%M").time()

        return real_time

   
    def retard(self):
        h_arrival =  self.arrival_time
        h_arrival_fixe = datetime.combine(h_arrival.date(), self.personnel.time_a)
        timezone = pytz.timezone('Africa/Douala')  # Par exemple, Africa/Douala

        # Ajoutez le fuseau horaire à l'objet datetime
        tolerance_datetime = h_arrival_fixe.replace(tzinfo=timezone)
     
        if h_arrival > tolerance_datetime:
           h_resultant_r=    h_arrival-tolerance_datetime
        else:
            h_d = "00:00"
            h_resultant_r = datetime.strptime(h_d,"%H:%M").time()


        return h_resultant_r
  
    
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
        return f"{self.user.username} - {self.date}"
class Zklecteur(models.Model):
    ip_adresse = models.CharField(max_length=32, unique=True)
    n_port = models.IntegerField(default='4370')

class Salaire(models.Model):
    date_month=models.DateField()
    montant = models.IntegerField()
    personnel= models.ForeignKey(Personnel,on_delete=models.CASCADE)
    def __str__(self):
        return f"Le {self.date_month} l'employé {Personnel.name} à percu {self.montant}"