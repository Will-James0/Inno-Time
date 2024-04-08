from django import forms
from .models import Personnel,Poste,Horaire

class Part1Form(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ['as_poste','nom_poste','somme','heure_debut','heure_fin']
  
  
class Part2Form(forms.ModelForm):
     class Meta:
        model = Personnel
        fields = ['name','prenom','email','gender','poste']
        labels = {'name':'Nom','prenom':'Prénom','email':'Email','gender':'Genre','poste':'Poste'}


class Part3Form(forms.ModelForm):
    
    class Meta:
        model = Horaire
        fields = ['arrival_time','departure_time','personnel']


