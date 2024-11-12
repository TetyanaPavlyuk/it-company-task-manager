# Generated by Django 5.0.6 on 2024-06-13 16:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0003_alter_task_options_alter_worker_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["is_completed", "deadline", "name"]},
        ),
        migrations.CreateModel(
            name="New",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="news",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-creation_date"],
            },
        ),
    ]
