# Generated by Django 5.1.7 on 2025-04-19 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role_permission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolepermission',
            name='model',
            field=models.CharField(default=True, max_length=50, null=True),
        ),
    ]
