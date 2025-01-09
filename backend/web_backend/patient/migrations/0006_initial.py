# Generated by Django 5.1.4 on 2025-01-09 11:42

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("patient", "0005_delete_patient"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("w", "woman"), ("m", "man")],
                        default="w",
                        max_length=1,
                    ),
                ),
                ("birthday", models.DateField(blank=True, null=True)),
                (
                    "phone_number",
                    models.CharField(
                        default="0000000000",
                        max_length=10,
                        validators=[
                            django.core.validators.RegexValidator(regex="^\\d{10}$")
                        ],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "city",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cities_light.city",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cities_light.country",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
