# Generated by Django 5.0.2 on 2024-04-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0010_alter_poste_heure_fin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zklecteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_adresse', models.CharField(max_length=32)),
                ('n_port', models.IntegerField(default='4370')),
            ],
        ),
    ]
