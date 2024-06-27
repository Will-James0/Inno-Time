from django import forms
from .models import Poste,Horaire,Zklecteur,Personnel
from datetime import time,date

# formulaire du poste
class Part1Form(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ['as_poste','name_poste','salary','start_time','end_time','tolerance_time','time_work']
  
# formulaire du personnel
class PersonnelForm(forms.ModelForm):
     class Meta:
        model = Personnel
        fields = ['name','first_name','email','gender','poste','time_works','salary','user']
        labels = {'name':'Nom','prenom':'Prénom','email':'Email','salary':'Plus value',
                  'heure_fixe':'Heure à effectuer','gender':'Genre','poste':'Poste','user':'User'}

# formulaire des horaires
class HoraireForm(forms.ModelForm):
    
    class Meta:
        
        model = Horaire
        fields = ['date_check','start_time','end_time','personnel','status','punch']
#         initial = {'date_d': date.today()}

       

class ZKTecoForm(forms.ModelForm):
    # ip_address = forms.CharField(label='Adresse IP')
    # port_number = forms.IntegerField(label='Numéro de port')
    class Meta:
        model=Zklecteur
        fields = ['ip_adresse','n_port']

