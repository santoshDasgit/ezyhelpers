# Generated by Django 4.2.3 on 2023-08-14 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_helperhistorymodel_admin_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historymodel',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.leadhistorymodel'),
        ),
    ]