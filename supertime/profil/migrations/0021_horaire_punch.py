# Generated by Django 5.0.2 on 2024-04-25 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0020_remove_horaire_punch_alter_personnel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='horaire',
            name='punch',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
    ]
