from random import choices
from tabnanny import verbose
from django.db import models
from datetime import datetime


# Create your models here.


class Personnel(models.Model):
    name = models.CharField(max_length=64,verbose_name="Nom")
    prenom = models.CharField(max_length=64,verbose_name="Prénom")
    email = models.EmailField(unique=True,verbose_name="Email")
    genre = models.CharField(max_length=100, choices=[('Masculin','Masculin'),('Feminin','Feminin')], verbose_name= "Genre")
    salaire = models.FloatField(verbose_name= "Salaire mensuel")
    arrival_time = models.TimeField(verbose_name="Time_IN")
    departure_time = models.TimeField(verbose_name="Time_OUT")
    duration = models.DurationField(null=True,blank=True)
    def save(self):
        arrival = datetime.combine(datetime.today(), self.arrival_time)
        departure = datetime.combine(datetime.today(), self.departure_time)

        duration = departure - arrival

        return duration
    class Meta:
        verbose_name ="Personnel"
        verbose_name_plural ="Personnels"
    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    date_j = models.DateField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    duree_j = models.TimeField()
    employee = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    def __str__(self):
        return self.date_j

class Poste(models.Model):
    as_poste = models.CharField(max_length=6,verbose_name="AS_Poste")
    nom_poste = models.CharField(max_length=62,verbose_name="Poste")
    somme = models.IntegerField()
    employee_p = models.ForeignKey(Personnel,on_delele=models.CASCADE)
    def __str__(self):
        return self.as_poste
    
class Classpersonnel(models.Model):
    posteIns = models.ForeignKey(Poste,on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE) 

    def __str__(self):
        return self.personnel.pk

    def get_present(self):
        personnel =  self.personnel
        _class =  self.posteIns
        try:
            present = Attendance.objects.filter(posteIns= _class, personnel=personnel, type = 1).count()
            return present
        except:
            return 0
    
    def get_tardy(self):
        personnel =  self.personnel
        _class =  self.posteIns
        try:
            present = Attendance.objects.filter(posteIns= _class, personnel=personnel, type = 2).count()
            return present
        except:
            return 0

    def get_absent(self):
        personnel =  self.personnel
        _class =  self.posteIns
        try:
            present = Attendance.objects.filter(posteIns= _class, personnel=personnel, type = 3).count()
            return present
        except:
            return 0

class Attendance(models.Model):
    posteIns = models.ForeignKey(Poste,on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    type = models.CharField(max_length=250, choices = [('1','Present'),('2','Tardy'),('1','Absent')] )
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.posteIns.nom_poste + "  " +self.personnel.pk

