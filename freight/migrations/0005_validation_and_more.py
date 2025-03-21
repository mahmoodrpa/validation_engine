# Generated by Django 5.1 on 2024-08-19 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freight', '0004_edi_actual_edi_master_freight_communication'),
    ]

    operations = [
        migrations.CreateModel(
            name='validation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.CharField(blank=True, max_length=255, null=True)),
                ('standard_customer', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_account', models.CharField(blank=True, max_length=255, null=True)),
                ('deduction_reference', models.CharField(blank=True, max_length=255, null=True)),
                ('deduction_date', models.DateField(blank=True, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=255, null=True)),
                ('deducted_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('deducted_qty', models.IntegerField(blank=True, null=True)),
                ('deducted_price_per_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('deduction_reason', models.TextField(blank=True, null=True)),
                ('billed_qty', models.CharField(blank=True, max_length=50, null=True)),
                ('gross_price_per_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('net_price_per_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('freight_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fuel_allowance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('lane', models.CharField(blank=True, max_length=255, null=True)),
                ('freight_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_freight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('freight_code_master', models.CharField(blank=True, max_length=255, null=True)),
                ('freight_code_actual', models.CharField(blank=True, max_length=255, null=True)),
                ('communicated_lane', models.CharField(blank=True, max_length=255, null=True)),
                ('communicated_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('communicated_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('missing_data', models.CharField(max_length=20, null=True)),
                ('no_shortage_in_pod', models.CharField(max_length=20, null=True)),
                ('invalid_amt_1', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('partial_shortage_in_pod', models.CharField(max_length=20, null=True)),
                ('invalid_amt_2', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('deducted_sku_is_not_invoiced', models.CharField(max_length=20, null=True)),
                ('invalid_amt_3', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('pricing_variance', models.CharField(max_length=20, null=True)),
                ('invalid_amt_4', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('validation_status', models.CharField(max_length=20, null=True)),
                ('invalid_amt', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('valid_amt', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('final_rca', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='edi_actual',
            old_name='freight_code',
            new_name='freight_code_actual',
        ),
        migrations.RenameField(
            model_name='edi_master',
            old_name='freight_code',
            new_name='freight_code_master',
        ),
        migrations.RenameField(
            model_name='freight_communication',
            old_name='lane',
            new_name='communicated_lane',
        ),
        migrations.RenameField(
            model_name='freight_communication',
            old_name='rate',
            new_name='communicated_rate',
        ),
        migrations.RenameField(
            model_name='freight_communication',
            old_name='weight',
            new_name='communicated_weight',
        ),
    ]
