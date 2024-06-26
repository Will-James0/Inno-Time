# Generated by Django 5.0.2 on 2024-05-02 08:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('as_poste', models.CharField(max_length=6, null=True, verbose_name='ALIAS_Poste')),
                ('nom_poste', models.CharField(max_length=62, null=True, verbose_name='Poste')),
                ('somme', models.IntegerField(default='2500', null=True)),
                ('heure_debut', models.TimeField(default='08:00', null=True)),
                ('heure_fin', models.TimeField(default='18:00', null=True)),
                ('tolerance_time', models.TimeField(default='08:30', null=True)),
                ('time_work', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zklecteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_adresse', models.CharField(max_length=32)),
                ('n_port', models.IntegerField(default='4370')),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, null=True, verbose_name='Nom')),
                ('prenom', models.CharField(max_length=64, null=True, verbose_name='Prénom')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='Email')),
                ('gender', models.CharField(choices=[('Masculin', 'Masculin'), ('Feminin', 'Feminin')], default='Masculin', max_length=100, null=True, verbose_name='Genre')),
                ('heure_fixe', models.IntegerField(default='100', null=True)),
                ('salary', models.FloatField(default='0', null=True)),
                ('time_a', models.TimeField(null=True)),
                ('time_s', models.TimeField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('poste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profil.poste', verbose_name='Poste')),
            ],
            options={
                'verbose_name': 'Personnel',
                'verbose_name_plural': 'Personnels',
            },
        ),
        migrations.CreateModel(
            name='Horaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_d', models.DateTimeField(null=True)),
                ('arrival_time', models.DateTimeField(null=True)),
                ('departure_time', models.DateTimeField(null=True)),
                ('status', models.CharField(blank=True, max_length=65, null=True)),
                ('statute', models.CharField(max_length=65, null=True)),
                ('punch', models.CharField(blank=True, max_length=65, null=True)),
                ('id_att', models.IntegerField(null=True)),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profil.personnel', verbose_name='Personnel')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_att', models.IntegerField(null=True, unique=True)),
                ('date', models.DateTimeField(null=True)),
                ('heure_punch', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=65, null=True)),
                ('punch', models.CharField(max_length=65, null=True)),
                ('personnel_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profil.personnel')),
            ],
        ),
    ]
