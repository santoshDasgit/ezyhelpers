# Generated by Django 4.2.3 on 2023-08-15 06:23

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_historymodel_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='helpermodel',
            name='id_pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/', validators=[app.models.validate_pdf]),
        ),
        migrations.AddField(
            model_name='helpermodel',
            name='id_type',
            field=models.CharField(blank=True, choices=[('dl', 'DL'), ('aadhar', 'AADHAR'), ('pan', 'PAN')], max_length=100, null=True),
        ),
    ]
