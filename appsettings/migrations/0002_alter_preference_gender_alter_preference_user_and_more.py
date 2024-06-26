# Generated by Django 5.0.2 on 2024-05-16 14:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsettings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='preference',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preference', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='temporarypreference',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='temporarypreference',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='temporary_preference', to=settings.AUTH_USER_MODEL),
        ),
    ]
