# Generated by Django 5.2 on 2025-04-16 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0002_initial'),
        ('user', '0002_rename_role_user_role_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role_id',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to='role.role'),
        ),
    ]
