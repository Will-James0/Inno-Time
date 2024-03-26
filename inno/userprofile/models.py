# from random import choices
# from tabnanny import verbose
# from django.db import models

# # Create your models here.
# class Personnel(models.Model):
#     name = models.CharField(max_length=64,verbose_name="Nom")
#     prenom = models.CharField(max_length=64,verbose_name="Prénom")
#     email = models.EmailField(unique=True,verbose_name="Email")
#     # genre = [('M','Masculin'),('F','Feminin')]
#     # sexe = models.TextChoices( choice=genre)
#     date_e = models.TimeField(auto_now=True ,max_length=12,verbose_name="Time_IN")
#     date_s = models.TimeField(auto_now=True ,max_length=12,verbose_name="Time_OUT")
#     class Meta:
#         verbose_name ="Personnel"
#         verbose_name_plural ="Personnels"
#     def __str__(self) -> str:
#         return self.name