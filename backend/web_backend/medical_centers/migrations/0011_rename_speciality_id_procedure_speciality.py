# Generated by Django 5.1.4 on 2025-01-15 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("medical_centers", "0010_rename_speciality_code_procedure_speciality_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="procedure",
            old_name="speciality_id",
            new_name="speciality",
        ),
    ]
