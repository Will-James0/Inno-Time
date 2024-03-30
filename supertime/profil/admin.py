from django.contrib import admin
from .models import models, Personnel,Poste,Horaire


# Register your models here.

@admin.register(Poste) 
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('id_poste','nom_poste','somme')
    list_filter = ['id_poste']
    
@admin.register(Horaire) 
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('jour','mois','nbre_d','heure_arrive','heure_sorti','duree')


@admin.register(Personnel) 
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('name','prenom','email','horaire_m','gender')
    search_fields = ['name']



