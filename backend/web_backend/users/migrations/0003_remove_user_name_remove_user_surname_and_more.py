# Generated by Django 5.1.4 on 2025-01-08 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="surname",
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=50),
        ),
    ]
