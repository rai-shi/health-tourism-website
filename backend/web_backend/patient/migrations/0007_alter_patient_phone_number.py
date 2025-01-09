# Generated by Django 5.1.4 on 2025-01-09 12:27

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("patient", "0006_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None
            ),
        ),
    ]
