# Generated by Django 4.1.7 on 2023-03-09 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                    "title",
                    models.CharField(
                        error_messages={
                            "unique": "A book with that title already exists."
                        },
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("author", models.CharField(max_length=255)),
                ("is_available", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ("title",),
            },
        ),
        migrations.CreateModel(
            name="Follow",
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
                ("will_be_available_date", models.DateTimeField(blank=True, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="books.book"
                    ),
                ),
            ],
        ),
    ]
