from django import forms
from .models import Personnel,Poste,Horaire
from datetime import time,date

class Part1Form(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ['as_poste','nom_poste','somme','heure_debut','heure_fin']
  
  
class Part2Form(forms.ModelForm):
     class Meta:
        model = Personnel
        fields = ['name','prenom','email','gender','poste','heure_fixe','salary']
        labels = {'name':'Nom','prenom':'Prénom','email':'Email','salary':'Plus value','heure_fixe':'Heure à effectuer','gender':'Genre','poste':'Poste'}


class Part3Form(forms.ModelForm):
    
    class Meta:
        
        model = Horaire
        fields = ['date_d','arrival_time','departure_time','personnel']
        initial = {'date_d': date.today()}
