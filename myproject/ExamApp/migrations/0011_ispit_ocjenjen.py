# Generated by Django 4.1.3 on 2023-01-03 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExamApp', '0010_odgovorzadatka_ispit'),
    ]

    operations = [
        migrations.AddField(
            model_name='ispit',
            name='ocjenjen',
            field=models.BooleanField(default=False),
        ),
    ]