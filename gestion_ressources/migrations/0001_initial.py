# Generated by Django 5.2 on 2025-04-09 16:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Demande",
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
                    "type_demande",
                    models.CharField(
                        choices=[
                            ("CONGE", "Congé"),
                            ("ABSENCE", "Absence"),
                            ("MISSION", "Mission"),
                        ],
                        max_length=10,
                    ),
                ),
                ("date_debut", models.DateField()),
                ("date_fin", models.DateField()),
                ("motif", models.TextField(blank=True, null=True)),
                (
                    "date_soumission",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("EN_ATTENTE", "En attente"),
                            ("APPROUVEE", "Approuvée"),
                            ("REJETEE", "Rejetée"),
                        ],
                        default="EN_ATTENTE",
                        max_length=10,
                    ),
                ),
                ("date_traitement", models.DateTimeField(blank=True, null=True)),
                ("commentaire_approbateur", models.TextField(blank=True, null=True)),
                (
                    "demandeur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="demandes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "traitee_par",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="demandes_traitees",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_soumission"],
            },
        ),
    ]
