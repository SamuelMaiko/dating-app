# Generated by Django 5.0.2 on 2024-05-16 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0005_alter_emailotp_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='transfer_completed',
            field=models.BooleanField(default=False),
        ),
    ]