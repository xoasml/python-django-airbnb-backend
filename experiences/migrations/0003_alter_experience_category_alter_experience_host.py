# Generated by Django 5.0.7 on 2024-07-22 04:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0002_alter_category_options"),
        ("experiences", "0002_experience_category_alter_perk_detail_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="experience",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="experiences",
                to="categories.category",
            ),
        ),
        migrations.AlterField(
            model_name="experience",
            name="host",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="experiences",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
