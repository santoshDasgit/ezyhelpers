# Generated by Django 4.2.3 on 2023-07-28 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_helpermodel_helper_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helpermodel',
            name='helper_status',
            field=models.CharField(choices=[('placed', 'Placed'), ('pending', 'Pending'), ('need_to_contact', 'Need to contact')], default='placed', max_length=50),
        ),
    ]