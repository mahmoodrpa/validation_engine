# Generated by Django 4.2.5 on 2024-08-06 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_user_data_first_login'),
    ]

    operations = [
        migrations.DeleteModel(
            name='deduction_data',
        ),
        migrations.DeleteModel(
            name='kroger_hrc',
        ),
        migrations.DeleteModel(
            name='vbrk',
        ),
        migrations.DeleteModel(
            name='vbrk_ref',
        ),
        migrations.DeleteModel(
            name='vbrp',
        ),
        migrations.DeleteModel(
            name='zoa',
        ),
    ]
