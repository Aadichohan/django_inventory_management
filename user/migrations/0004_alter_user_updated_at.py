# Generated by Django 5.2 on 2025-04-16 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_user_role_id_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
