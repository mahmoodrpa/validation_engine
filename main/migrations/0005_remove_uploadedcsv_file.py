# Generated by Django 4.2.5 on 2023-09-07 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_uploadedcsv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedcsv',
            name='file',
        ),
    ]
