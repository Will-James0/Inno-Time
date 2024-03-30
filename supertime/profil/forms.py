from django import forms
from .models import Personnel,Poste

class ProfilForm(forms.ModelForm):
  
   poste = forms.ModelChoiceField(queryset= Poste.objects.all(),label="Poste")
   class Meta:
        model = Personnel
        fields = ['name','prenom','email','gender','poste']
        labels = {'name':'Nom','prenom':'Prénom','email':'Email','gender':'Genre','poste':'Poste'}
