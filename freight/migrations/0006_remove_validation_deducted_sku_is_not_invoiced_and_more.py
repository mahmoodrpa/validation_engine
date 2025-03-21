# Generated by Django 5.1 on 2024-08-19 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freight', '0005_validation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='validation',
            name='deducted_sku_is_not_invoiced',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='final_rca',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='invalid_amt',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='invalid_amt_1',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='invalid_amt_2',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='invalid_amt_3',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='invalid_amt_4',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='missing_data',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='no_shortage_in_pod',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='partial_shortage_in_pod',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='pricing_variance',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='valid_amt',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='validation_status',
        ),
    ]
