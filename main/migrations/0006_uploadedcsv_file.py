# Generated by Django 4.2.5 on 2023-09-07 19:11

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_uploadedcsv_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedcsv',
            name='file',
            field=models.FileField(default='NoFile.csv', upload_to=main.models.custom_upload_path),
        ),
    ]
