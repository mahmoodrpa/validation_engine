# Generated by Django 4.2.5 on 2024-09-13 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osd', '0005_validation_carrier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='validation',
            old_name='final_rca',
            new_name='invalid_reason',
        ),
    ]
