# Generated by Django 4.1.3 on 2022-11-28 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExamApp', '0003_remove_ispit_pitanja_pitanja_ispit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='zadavac',
            name='broj_neocjenjenih_ispita',
            field=models.IntegerField(default=0),
        ),
    ]
