# Generated by Django 5.1.7 on 2025-04-17 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='unit_price',
        ),
    ]
