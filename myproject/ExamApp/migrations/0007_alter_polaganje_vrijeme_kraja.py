# Generated by Django 4.1.3 on 2022-12-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExamApp', '0006_alter_polaganje_vrijeme_kraja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polaganje',
            name='vrijeme_kraja',
            field=models.TimeField(blank=True, null=True),
        ),
    ]