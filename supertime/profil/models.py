from django.db import models
from datetime import datetime,date
import time
from django.contrib.auth.models import User
import pytz
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(AbstractUser):
#     code_id_user=models.CharField(max_length=15)

class Poste(models.Model):
    as_poste = models.CharField(max_length=60,verbose_name="ALIAS_Poste",null=True)
    name_poste = models.CharField(max_length=62,verbose_name="Poste",null=True)
    salary= models.FloatField(null=True)
    start_time= models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    tolerance_time=models.TimeField( null=True)
    time_work = models.IntegerField(null = True)
    def __str__(self):
        return self.as_poste



class Personnel(models.Model):
    # nom de l'emplouyés
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64,verbose_name="Nom",null=True)
    # prénom de l'emplouyés
    first_name = models.CharField(max_length=64,verbose_name="Prénom",null=True)
    # email de l'emplouyés
    email = models.EmailField(unique=True,verbose_name="Email",null=True)
    #horaire_m = models.IntegerField(null=True,verbose_name="Horaire menseule")
    # poste auccupé par l'emplouyés
    poste = models.ForeignKey(Poste,on_delete=models.CASCADE,verbose_name="Poste")
    # nom de l'emplouyés
    gender = models.CharField(default='Masculin',max_length=100, choices=[('Masculin','Masculin'),('Feminin','Feminin')],verbose_name="Genre", null=True)
    time_works = models.IntegerField(default='100',null=True)# n
    salary = models.FloatField(default='0',null=True) # n
    start_time = models.TimeField(null = True)
    tolerance_time=models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    photo = models.ImageField(upload_to='photo_user/', blank=True, null=True)
    
    class Meta:
        verbose_name ="Personnel"
        verbose_name_plural ="Personnels"
    def __str__(self):
        return self.name
    def get_self(self):
        return Personnel.objects.get(user = self.user)

class Horaire(models.Model):
    date_check = models.DateTimeField(null=True) # n
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE,verbose_name="Personnel")
    status = models.CharField(max_length=65,null=True, blank=True)
    statute = models.CharField(max_length=65, null= True)
    punch = models.CharField(max_length=65,null=True, blank=True)
    # id_att=models.IntegerField(null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    #date_days = models.DateTimeField(auto_now=True null=True)

    def calculate_duration(self):
        timezone = pytz.timezone('Africa/Douala')  # Par exemple, Africa/Douala
        check_in_time = self.start_time
        check_out_time = self.end_time

        # Si check_out_time est None, définissez la durée à 00:00:00
        if check_out_time is None:
            check_out_time_default = datetime.strptime("00:00:00", "%H:%M:%S").time()
            return check_out_time_default.replace(tzinfo=timezone)

        start_time = datetime.combine(check_in_time.date(), self.personnel.start_time).replace(tzinfo=timezone)
        end_time = datetime.combine(check_out_time.date(), self.personnel.end_time).replace(tzinfo=timezone)
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
            real_time = datetime.strptime("00:00:00", "%H:%M:%S").time()

        return real_time.replace(tzinfo=timezone)

   
    def retard(self):
        h_arrival =  self.start_time
        h_arrival_fixe = datetime.combine(h_arrival.date(), self.personnel.start_time)
        timezone = pytz.timezone('Africa/Douala')  # Par exemple, Africa/Douala

        # Ajoutez le fuseau horaire à l'objet datetime
        tolerance_datetime = h_arrival_fixe.replace(tzinfo=timezone)
     
        if h_arrival > tolerance_datetime:
           h_resultant_r=    h_arrival-tolerance_datetime
        else:
            
            h_resultant_r = datetime.strptime("00:00:00", "%H:%M:%S").time()


        return h_resultant_r.replace(tzinfo=timezone)
  
    
    def __str__(self):
        return self.pk
 
class Zklecteur(models.Model):
    ip_adresse = models.CharField(max_length=32, unique=True)
    n_port = models.IntegerField(default='4370')
    model_drive = models.CharField(max_length=64,null=True,)   

class Attendance(models.Model):
    personnel_a = models.ForeignKey(Personnel,on_delete=models.CASCADE)
    # id_att=models.IntegerField(unique=True,null=True)
    id_att=models.IntegerField(null=True)
    date = models.DateTimeField(null=True)
    heure_punch = models.DateTimeField(null=True, )
    status = models.CharField(max_length=65,null=True, )
    punch = models.CharField(max_length=65,null=True, )
    # Autres champs pour les informations de présence
    lecteur = models.ForeignKey(Zklecteur,on_delete=models.CASCADE,null=True,)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Salaire(models.Model):
    date_month=models.DateField()
    montant = models.IntegerField()
    personnel= models.ForeignKey(Personnel,on_delete=models.CASCADE)
    time_work=models.IntegerField()
    def __str__(self):
        return f"Le {self.date_month} l'employé {Personnel.name} à percu {self.montant}"

#     from django.db import models
# from django.contrib.auth.models import User

# class Employe(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     taux_horaire = models.DecimalField(max_digits=5, decimal_places=2)

#     def __str__(self):
#         return self.user.username

# class Attendance(models.Model):
#     employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
#     date = models.DateField()
#     heure_entree = models.TimeField()
#     heure_sortie = models.TimeField()

#     def __str__(self):
#         return f"{self.employe} - {self.date}"

# class Salaire(models.Model):
#     employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
#     date = models.DateField()
#     montant = models.DecimalField(max_digits=8, decimal_places=2)

#     def __str__(self):
#         return f"{self.employe} - {self.date}"