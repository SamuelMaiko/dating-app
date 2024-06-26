# Generated by Django 5.0.2 on 2024-05-16 14:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_age', models.IntegerField(default=18)),
                ('max_age', models.IntegerField(default=100)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], max_length=10)),
                ('denomination', models.CharField(blank=True, choices=[('CTH', 'Catholic'), ('ADV', 'Adventist'), ('ISL', 'Islamic'), ('PRO', 'Protestant'), ('OTH', 'Other')], max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'preferences',
            },
        ),
        migrations.CreateModel(
            name='TemporaryPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_age', models.IntegerField(default=18)),
                ('max_age', models.IntegerField(default=100)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], max_length=10)),
                ('denomination', models.CharField(blank=True, choices=[('CTH', 'Catholic'), ('ADV', 'Adventist'), ('ISL', 'Islamic'), ('PRO', 'Protestant'), ('OTH', 'Other')], max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'temporary_preferences',
            },
        ),
    ]
