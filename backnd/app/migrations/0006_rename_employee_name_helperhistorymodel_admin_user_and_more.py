# Generated by Django 4.2.3 on 2023-08-10 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_helperhistorymodel_employee_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='helperhistorymodel',
            old_name='employee_name',
            new_name='admin_user',
        ),
        migrations.RenameField(
            model_name='helpermodel',
            old_name='employee_name',
            new_name='admin_user',
        ),
    ]
