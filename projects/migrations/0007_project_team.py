# Generated by Django 5.2 on 2025-05-07 07:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_owner'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='teams.team'),
        ),
    ]
