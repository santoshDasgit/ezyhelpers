# Generated by Django 4.2.3 on 2023-07-14 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_leadmodel_contact_status_leadmodel_lead_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadmodel',
            name='lead_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
