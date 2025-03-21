# Generated by Django 5.1 on 2024-09-09 22:35

import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='validation',
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
                ('billed_qty', models.CharField(blank=True, max_length=50, null=True)),
                ('gross_price_per_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('net_price_per_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
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
                ('invalid_amt', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('valid_amt', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('final_rca', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='backup_data',
            name='ids',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='deduction_data',
            name='ids',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice_data',
            name='freight_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='invoice_data',
            name='freight_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pod_detail',
            name='pod_file',
            field=models.FileField(default='NoFile.pdf', upload_to=main.models.custom_upload_path),
        ),
        migrations.AlterField(
            model_name='backup_data',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='deduction_data',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='deduction_data',
            name='standard_customer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoice_data',
            name='billed_qty',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pod_detail',
            name='invoice_number',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pod_detail',
            name='pod_found',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pod_detail',
            name='sku',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pod_detail',
            name='subject_to_count',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
