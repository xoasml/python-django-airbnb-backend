from django.contrib import admin
from .models import Experience, Perk


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "start",
        "end",
        "created_at",
        "updated_at",
    )


@admin.register(Perk)
class PerksAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "detail",
        "explanation",
    )
