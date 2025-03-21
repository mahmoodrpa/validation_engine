# Generated by Django 5.1 on 2024-09-08 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0002_backup_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='price_change',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pack_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('case_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('units_per_case', models.IntegerField(blank=True, null=True)),
                ('units_per_pack', models.IntegerField(blank=True, null=True)),
                ('packs_per_case', models.IntegerField(blank=True, null=True)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('communication_date', models.DateField(blank=True, null=True)),
                ('buyer_approved', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=3)),
            ],
        ),
    ]
