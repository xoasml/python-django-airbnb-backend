# Generated by Django 5.0.7 on 2024-07-22 04:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0003_alter_experience_category_alter_experience_host"),
        ("medias", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="experience",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="experiences.experience",
            ),
        ),
        migrations.AlterField(
            model_name="photo",
            name="file",
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name="photo",
            name="room",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="experience",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="video",
                to="experiences.experience",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="file",
            field=models.URLField(),
        ),
    ]
