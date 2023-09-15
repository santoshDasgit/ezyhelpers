# Generated by Django 4.2.3 on 2023-08-19 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_helpermodel_availability_status_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelperJobRoleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.CharField(max_length=100)),
                ('helper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.helpermodel')),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalQualificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(max_length=100)),
                ('helper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.helpermodel')),
            ],
        ),
    ]