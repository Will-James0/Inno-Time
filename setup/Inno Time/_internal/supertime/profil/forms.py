from django import forms
from .models import Poste,Horaire,Zklecteur,Personnel
from datetime import time,date

# formulaire du poste
class Part1Form(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ['as_poste','nom_poste','somme','heure_debut','heure_fin']
  
# formulaire du personnel
class Part2Form(forms.ModelForm):
     class Meta:
        model = Personnel
        fields = ['name','prenom','email','gender','poste','heure_fixe','salary','user']
        labels = {'name':'Nom','prenom':'Prénom','email':'Email','salary':'Plus value',
                  'heure_fixe':'Heure à effectuer','gender':'Genre','poste':'Poste','user':'User'}

# formulaire des horaires
class Part3Form(forms.ModelForm):
    
    class Meta:
        
        model = Horaire
        fields = ['date_d','arrival_time','departure_time','personnel','status','punch','id_att']
#         initial = {'date_d': date.today()}

       

class ZKTecoForm(forms.ModelForm):
    # ip_address = forms.CharField(label='Adresse IP')
    # port_number = forms.IntegerField(label='Numéro de port')
    class Meta:
        model=Zklecteur
        fields = ['ip_adresse','n_port']

