# Generated by Django 5.0.2 on 2024-05-25 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobbie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'hobbies',
            },
        ),
        migrations.CreateModel(
            name='HobbieProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobbie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hobbie_profile', to='profiles.hobbie')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hobbie_profile', to='profiles.userprofile')),
            ],
            options={
                'db_table': 'hobbie_profile',
                'unique_together': {('profile', 'hobbie')},
            },
        ),
    ]
