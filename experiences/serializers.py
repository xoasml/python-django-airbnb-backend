from rest_framework import serializers
from .models import Perk, Experience
from categories.models import Category


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "photos",
        )

    def get_rating(self, experiences):
        return experiences.rating()


class CreateExperienceSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)

    class Meta:
        model = Experience
        fields = (
            "country",
            "city",
            "name",
            "price",
            "address",
            "start",
            "end",
            "description",
            "perks",
            "category",
        )

    def validate_category(self, value):

        if value.kind != Category.CategoryKindChoices.EXPERIENCES:
            raise serializers.ValidationError("올바른 experience category를 골라주세요")

        return value

    def validate(self, data):
        request = self.context.get("request")
        user = request.user

        if not user.is_host:
            raise serializers.ValidationError("호스트 계정이 아닙니다.")

        if data["start"] < data["end"]:
            raise serializers.ValidationError("end 보다 start 이 작아야 합니다. ")

        return data
