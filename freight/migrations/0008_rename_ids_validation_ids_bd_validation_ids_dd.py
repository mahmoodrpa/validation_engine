# Generated by Django 5.1 on 2024-08-20 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freight', '0007_validation_gross_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='validation',
            old_name='ids',
            new_name='ids_bd',
        ),
        migrations.AddField(
            model_name='validation',
            name='ids_dd',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
