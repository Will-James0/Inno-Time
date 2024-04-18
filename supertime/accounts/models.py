from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from profil.models import Poste

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    genre = models.CharField(max_length=10)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photo_user/', blank=True)

    def get_self(self):
        return Profile.objects.get(user = self.user)