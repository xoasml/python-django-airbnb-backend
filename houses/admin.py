from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    # 상세화면 구조 설정
    fields = (
        "name", # 첫줄에 name 1개
        "address", # 다음줄 address 1개
        ("price_per_night", "pet_allowed"), #다음 줄 price, pet 2개
    )

    # admin 페이지 검색 설정
    search_fields = ("address",)

    # admin 페이지 그리드에 표현될 필드 설정
    list_display = (
        "name",
        "price_per_night",
        "address",
        "pet_allowed",
    )

    # admin 페이지 조회 필터 설정
    list_filter = (
        "price_per_night",
        "pet_allowed",
    )

    # 리스트에서 상세 화면 링크 설정할 필드 설정
    list_display_links = ("name", "address",)

    # 리스트에서 데이터 수정 가능 설정
    list_editable = ("pet_allowed",)


