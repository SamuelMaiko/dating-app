# Generated by Django 5.0.2 on 2024-05-26 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0017_alter_hobbie_profiles'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='favorite',
            table='favorites',
        ),
    ]
