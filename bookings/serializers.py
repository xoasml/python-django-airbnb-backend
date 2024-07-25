from django.utils import timezone
from rest_framework import serializers
from .models import Booking
from rooms.serializers import TinyRoomSerializer


class CreateBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField(required=True)
    check_out = serializers.DateField(required=True)

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError(
                f"지나간 날짜에는 예약할 수 없어요 {value}"
            )
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError(
                f"지나간 날짜에는 예약할 수 없어요 {value}"
            )
        return value

    def validate(self, attrs):
        if attrs["check_out"] <= attrs["check_in"]:
            raise serializers.ValidationError("체크인은 체크아웃 보다 작아야 합니다.")

        if Booking.objects.filter(
            check_in__lte=attrs["check_out"],
            check_out__gte=attrs["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "이 날짜 (일부날짜)가 이미 예약돼있습니다."
            )

        return attrs


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class UsersBookingSerializer(serializers.ModelSerializer):

    room = TinyRoomSerializer()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "experience_time",
            "room",
        )
