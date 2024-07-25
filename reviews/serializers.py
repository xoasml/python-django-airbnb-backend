from rest_framework import serializers
from users.serializers import TinyUserSerializer
from rooms.serializers import TinyRoomSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )


class UsersRoomReviewSerializer(serializers.ModelSerializer):

    room = TinyRoomSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "room",
            "payload",
            "rating",
        )
