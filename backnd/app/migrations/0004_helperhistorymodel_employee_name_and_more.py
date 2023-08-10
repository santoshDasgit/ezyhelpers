# Generated by Django 4.2.3 on 2023-08-10 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_helperhistorymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='helperhistorymodel',
            name='employee_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.employeemodel'),
        ),
        migrations.AddField(
            model_name='helpermodel',
            name='employee_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.employeemodel'),
        ),
    ]
