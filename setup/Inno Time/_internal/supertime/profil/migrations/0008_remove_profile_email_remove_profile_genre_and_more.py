# Generated by Django 5.0.2 on 2024-05-16 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0007_alter_poste_somme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='poste',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='prenom',
        ),
    ]
