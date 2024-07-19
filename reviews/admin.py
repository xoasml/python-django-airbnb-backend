from django.contrib import admin
from .models import Review


class WordFileter(admin.SimpleListFilter):
    title = "Filter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("gggg", "gggg"),
            ("야미", "야미"),
            ("좋아요", "좋아요"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else :
            return reviews


# 나쁜 리뷰 3점 미만 / 좋은 리뷰 3점 이상 필터 만들기

class UpDownFilter(admin.SimpleListFilter):
    title = "rating 3up 3down"

    parameter_name = "updown"

    def lookups(self, request, reviews):
        return [
            ("up", "3up"),
            ("down", "3down")
        ]

    def queryset(self, request, reviews):
        updown = self.value()
        if updown == "up":
            return reviews.filter(rating__gte=3)
        elif updown == "down":
            return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        "user",
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
        WordFileter,
        UpDownFilter,
    )
