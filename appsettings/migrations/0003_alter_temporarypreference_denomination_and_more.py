# Generated by Django 5.0.2 on 2024-05-16 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsettings', '0002_alter_preference_gender_alter_preference_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporarypreference',
            name='denomination',
            field=models.CharField(blank=True, choices=[('Catholic', 'Catholic'), ('Adventist', 'Adventist'), ('Islamic', 'Islamic'), ('Protestant', 'Protestant'), ('Other', 'Other')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='temporarypreference',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True),
        ),
    ]
