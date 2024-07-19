from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    """Photo Model Definition"""

    file = models.ImageField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    def __str__(selfs) -> str:
        return "Photo File"


class Video(CommonModel):
    """Video Model Definition"""

    file = models.FileField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="video"
    )

    def __str__(self) -> str:
        return "Video File"
