from django.contrib import admin
from .models import Profile

@admin.register(Profile) 
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('user' ,'nom', 'prenom', 'email', 'genre', 'poste', 'photo')
    search_fields = ['user']

