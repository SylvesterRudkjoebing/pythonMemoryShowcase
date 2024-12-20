# Generated by Django 4.2.16 on 2024-11-27 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("event", models.CharField(max_length=255)),
                ("year", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("birth", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Participation",
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
                    "event",
                    models.ForeignKey(
                        db_column="event_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participants",
                        to="memoryAPI.event",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        db_column="person_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participations",
                        to="memoryAPI.person",
                    ),
                ),
            ],
        ),
    ]
