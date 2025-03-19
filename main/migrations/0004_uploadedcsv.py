# Generated by Django 4.2.5 on 2023-09-07 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_uploadrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedCSV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='csv_uploads/')),
                ('num_rows', models.PositiveIntegerField()),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('total_time', models.DurationField(blank=True, null=True)),
                ('current_status', models.CharField(choices=[('started', 'Started'), ('inprogress', 'In Progress'), ('completed', 'Completed')], default='started', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
