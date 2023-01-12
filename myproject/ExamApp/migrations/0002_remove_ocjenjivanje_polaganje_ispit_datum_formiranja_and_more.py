# Generated by Django 4.1.3 on 2022-11-28 18:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ExamApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ocjenjivanje',
            name='polaganje',
        ),
        migrations.AddField(
            model_name='ispit',
            name='datum_formiranja',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ispit',
            name='zadavac',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ExamApp.zadavac'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ocjenjivanje',
            name='ispit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ExamApp.ispit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ocjenjivanje',
            name='polagac',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ExamApp.polagac'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ispit',
            name='bodovi_info',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ExamApp.bodoviinfo'),
        ),
        migrations.DeleteModel(
            name='Formiranje',
        ),
    ]
