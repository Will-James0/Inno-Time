# Generated by Django 5.0.6 on 2024-06-10 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='horaire',
            old_name='arrival_time',
            new_name='date_check',
        ),
        migrations.RenameField(
            model_name='horaire',
            old_name='date_d',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='horaire',
            old_name='departure_time',
            new_name='start_time',
        ),
        migrations.RenameField(
            model_name='personnel',
            old_name='time_a',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='personnel',
            old_name='prenom',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='personnel',
            old_name='time_s',
            new_name='start_time',
        ),
        migrations.RenameField(
            model_name='personnel',
            old_name='heure_fixe',
            new_name='time_works',
        ),
        migrations.RenameField(
            model_name='poste',
            old_name='nom_poste',
            new_name='name_poste',
        ),
        migrations.RemoveField(
            model_name='horaire',
            name='id_att',
        ),
        migrations.RemoveField(
            model_name='poste',
            name='heure_debut',
        ),
        migrations.RemoveField(
            model_name='poste',
            name='heure_fin',
        ),
        migrations.RemoveField(
            model_name='poste',
            name='somme',
        ),
        migrations.AddField(
            model_name='personnel',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photo_user/'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='tolerance_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='poste',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='poste',
            name='salary',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='poste',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='poste',
            name='as_poste',
            field=models.CharField(max_length=60, null=True, verbose_name='ALIAS_Poste'),
        ),
        migrations.AlterField(
            model_name='poste',
            name='tolerance_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='zklecteur',
            name='ip_adresse',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.CreateModel(
            name='Salaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_month', models.DateField()),
                ('montant', models.IntegerField()),
                ('time_work', models.IntegerField()),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profil.personnel')),
            ],
        ),
    ]