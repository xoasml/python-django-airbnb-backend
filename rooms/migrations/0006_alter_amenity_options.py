# Generated by Django 5.0.7 on 2024-07-22 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0005_alter_room_amenities_alter_room_category_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="amenity",
            options={"verbose_name_plural": "amenities"},
        ),
    ]
