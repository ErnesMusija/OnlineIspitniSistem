# Generated by Django 4.1.3 on 2023-01-04 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExamApp', '0013_ocjenjivanje_ocjenjen'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ocjenainfo',
            old_name='min_prolazna_ocjena',
            new_name='min_ocjena',
        ),
        migrations.AlterUniqueTogether(
            name='ocjenainfo',
            unique_together={('max_ocjena', 'min_ocjena')},
        ),
    ]
