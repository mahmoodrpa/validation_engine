# Generated by Django 4.2.5 on 2024-09-18 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osd', '0007_validation_combined_shipment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction_data',
            name='validation_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
