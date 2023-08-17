# Generated by Django 4.2.3 on 2023-08-12 05:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0009_delete_helperhistorymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelperHistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('helper_id', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('helper_status', models.CharField(choices=[('placed', 'Placed'), ('pending', 'Pending'), ('need_to_contact', 'Need to contact')], default='pending', max_length=50)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('primary_phone', models.IntegerField()),
                ('secondary_phone', models.IntegerField(blank=True, null=True)),
                ('email_id', models.CharField(blank=True, default='Name@ezyhelpers.com', max_length=100, null=True)),
                ('dob', models.DateField()),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(choices=[('andhra_pradesh', 'Andhra Pradesh'), ('arunachal_pradesh', 'Arunachal Pradesh'), ('assam', 'Assam'), ('bihar', 'Bihar'), ('chhattisgarh', 'Chhattisgarh'), ('goa', 'Goa'), ('gujarat', 'Gujarat'), ('haryana', 'Haryana'), ('himachal_pradesh', 'Himachal Pradesh'), ('jharkhand', 'Jharkhand'), ('karnataka', 'Karnataka'), ('kerala', 'Kerala'), ('madhya_pradesh', 'Madhya Pradesh'), ('maharashtra', 'Maharashtra'), ('manipur', 'Manipur'), ('meghalaya', 'Meghalaya'), ('mizoram', 'Mizoram'), ('nagaland', 'Nagaland'), ('odisha', 'Odisha'), ('punjab', 'Punjab'), ('rajasthan', 'Rajasthan'), ('sikkim', 'Sikkim'), ('tamil_nadu', 'Tamil Nadu'), ('telangana', 'Telangana'), ('tripura', 'Tripura'), ('uttar_pradesh', 'Uttar Pradesh'), ('uttarakhand', 'Uttarakhand'), ('west_bengal', 'West Bengal')], max_length=100)),
                ('country', models.CharField(choices=[('india', 'INDIA')], max_length=100)),
                ('additional_comment', models.TextField(blank=True, null=True)),
                ('work_experience', models.CharField(choices=[('0-3 month', '0-3 month'), ('3-6 month', '3-6 month'), ('6-9 month', '6-9 month'), ('1 year', '1 year'), ('1.5 year', '1.5 year'), ('2 year', '2 year'), ('2.5 year', '2.5 year'), ('3 year', '3 year'), ('3.5 year', '3.5 year'), ('4 year', '4 year'), ('4.5 year', '4.5 year'), ('5 year', '5 year'), ('5.5 year', '5.5 year'), ('6 year', '6 year'), ('6.5 year', '6.5 year'), ('6 year+', '6 year+')], max_length=30)),
                ('availability_status_week', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], default=1)),
                ('availability_status', models.CharField(choices=[('live_in', 'Live in'), ('on_demand', 'On demand'), ('full_time', 'Full time'), ('part_time', 'Part time'), ('misc', 'Misc')], max_length=60)),
                ('locality', models.CharField(choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')], max_length=30)),
                ('near_by', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('history_status', models.CharField(choices=[('create', 'create'), ('delate', 'delete'), ('update', 'update')], default='create', max_length=100)),
                ('admin_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
