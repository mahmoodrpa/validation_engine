# Generated by Django 4.2.5 on 2024-09-13 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osd', '0004_deduction_data_deduction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='validation',
            name='carrier',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
