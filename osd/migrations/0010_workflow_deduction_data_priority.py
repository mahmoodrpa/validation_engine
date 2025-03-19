# Generated by Django 4.2.5 on 2024-09-23 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osd', '0009_rename_invalid_amt_validation_invalid_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='workflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.CharField(blank=True, max_length=255, null=True)),
                ('standard_customer', models.CharField(blank=True, max_length=255, null=True)),
                ('deduction_reference', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=255, null=True)),
                ('sku', models.CharField(blank=True, max_length=255, null=True)),
                ('deducted_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('deducted_qty', models.IntegerField(blank=True, null=True)),
                ('deducted_price_per_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('deduction_date', models.DateField(blank=True, null=True)),
                ('deduction_reason', models.TextField(blank=True, null=True)),
                ('billed_qty', models.IntegerField(blank=True, null=True)),
                ('gross_price_per_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('net_price_per_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('carrier', models.CharField(blank=True, max_length=255, null=True)),
                ('shortage', models.IntegerField(blank=True, null=True)),
                ('damage', models.IntegerField(blank=True, null=True)),
                ('returns', models.IntegerField(blank=True, null=True)),
                ('overage', models.IntegerField(blank=True, null=True)),
                ('net_shortage', models.IntegerField(blank=True, null=True)),
                ('customer_sign', models.CharField(blank=True, max_length=255, null=True)),
                ('carrier_sign', models.CharField(blank=True, max_length=255, null=True)),
                ('subject_to_count', models.CharField(blank=True, max_length=255, null=True)),
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
                ('invalid_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('valid_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('invalid_reason', models.CharField(blank=True, max_length=50, null=True)),
                ('product_substitution', models.CharField(blank=True, max_length=50, null=True)),
                ('combined_shipment', models.CharField(blank=True, max_length=50, null=True)),
                ('order_split', models.CharField(blank=True, max_length=50, null=True)),
                ('load_sequencing', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_of_measurement', models.CharField(blank=True, max_length=50, null=True)),
                ('deducted_at_higher_price', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='deduction_data',
            name='priority',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
