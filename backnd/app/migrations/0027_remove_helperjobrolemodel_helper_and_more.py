# Generated by Django 4.2.3 on 2023-08-19 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_helperjobrolemodel_additionalqualificationmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helperjobrolemodel',
            name='helper',
        ),
        migrations.DeleteModel(
            name='AdditionalQualificationModel',
        ),
        migrations.DeleteModel(
            name='HelperJobRoleModel',
        ),
    ]
