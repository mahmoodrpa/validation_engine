# Generated by Django 4.2.5 on 2024-09-24 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osd', '0012_workflow_billback_date_workflow_billback_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='billback_package',
            field=models.FileField(default='NoFile.zip', upload_to='media/billback_packages/'),
        ),
    ]
