# Generated by Django 5.1 on 2024-08-19 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freight', '0003_invoice_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='edi_actual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=255, null=True)),
                ('deduction_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('freight_code', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='edi_master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deduction_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('freight_code', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='freight_communication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_account', models.CharField(blank=True, max_length=255, null=True)),
                ('standard_customer', models.CharField(blank=True, max_length=255, null=True)),
                ('lane', models.CharField(blank=True, max_length=255, null=True)),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
    ]
