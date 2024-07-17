from django.db import models


class House(models.Model):
    """Model Definition for Houses"""

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField(verbose_name="Price", help_text="Positive numbers only")
    description = models.TextField()
    address = models.CharField(max_length=140)
    pet_allowed = models.BooleanField(
        verbose_name="Pet", # 보여지는 컬럼 문구
        default=True, # 디폴트
        help_text="can with pet?", # 설명 문구
    )

    def __str__(self):
        return self.name
