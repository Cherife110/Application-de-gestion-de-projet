# Generated by Django 4.2.1 on 2023-08-26 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
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
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
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
                ("title", models.CharField(max_length=200)),
                ("file", models.FileField(upload_to="projects/")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("EN", "En cours"),
                            ("SO", "Soumis"),
                            ("CO", "Corrigé"),
                            ("TR", "Traité"),
                            ("AR", "Archivé"),
                        ],
                        default="EN",
                        max_length=2,
                    ),
                ),
                ("feedback", models.TextField(blank=True)),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.subject",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PreviousProject",
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
                ("summary", models.TextField()),
                ("archived", models.BooleanField(default=False)),
                (
                    "project",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.project",
                    ),
                ),
            ],
        ),
    ]
