# Generated by Django 5.1.6 on 2025-04-12 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_rename_price_booking_booking_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='booking_price',
            new_name='price',
        ),
    ]
