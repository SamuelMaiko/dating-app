# Generated by Django 5.0.2 on 2024-05-24 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_alter_userphoto_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userphoto',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='user-photos/'),
        ),
    ]
