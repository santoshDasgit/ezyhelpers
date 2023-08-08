# Generated by Django 4.2.3 on 2023-08-07 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_helpermodel_locality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helpermodel',
            name='locality',
            field=models.CharField(blank=True, choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'), (None, None)], default=None, max_length=30, null=True),
        ),
    ]
