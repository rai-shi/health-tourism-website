# Generated by Django 5.1.4 on 2025-01-17 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("destinations", "0002_rename_city_destination"),
        ("medical_centers", "0013_alter_medicalcenterphotos_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medicalcenter",
            name="city",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="medical_centers_city",
                to="destinations.destination",
            ),
        ),
    ]
