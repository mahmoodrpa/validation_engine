# Generated by Django 4.2.5 on 2023-11-16 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_vbrk_ref'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vbrk_ref',
            old_name='costco',
            new_name='Costco',
        ),
        migrations.RenameField(
            model_name='vbrk_ref',
            old_name='field_name',
            new_name='field_names',
        ),
    ]
