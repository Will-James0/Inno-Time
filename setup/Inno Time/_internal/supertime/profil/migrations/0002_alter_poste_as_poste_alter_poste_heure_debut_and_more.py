# Generated by Django 5.0.2 on 2024-05-02 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poste',
            name='as_poste',
            field=models.CharField(max_length=60, null=True, verbose_name='ALIAS_Poste'),
        ),
        migrations.AlterField(
            model_name='poste',
            name='heure_debut',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='poste',
            name='heure_fin',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='poste',
            name='somme',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='poste',
            name='tolerance_time',
            field=models.TimeField(null=True),
        ),
    ]
