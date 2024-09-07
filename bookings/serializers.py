from django.utils import timezone
from rest_framework import serializers
from .models import Booking
from rooms.serializers import TinyRoomSerializer


class CreateExperiencesBookingSerializer(serializers.ModelSerializer):

    experience_date = serializers.DateField(required=True)
    guests = serializers.IntegerField(required=True)

    class Meta:
        model = Booking
        fields = (
            "experience_date",
            "guests",
        )

    def validate_experience_date(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now >= value:
            raise serializers.ValidationError("현재 날짜 이후에 예약 할 수 있습니다.")

        return value

    def validate(self, data):
        if Booking.objects.filter(
            experience_date=data["experience_date"],
            experience=self.context["experience"],
        ).exists():
            raise serializers.ValidationError("예약이 마감 됐습니다.")

        return data


class CreateRoomsBookingSerializer(serializers.ModelSerializer):

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
        room = self.context.get("room")
        if attrs["check_out"] <= attrs["check_in"]:
            raise serializers.ValidationError("체크인은 체크아웃 보다 작아야 합니다.")

        if Booking.objects.filter(
            room=room,
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
            "experience_date",
            "guests",
        )


class UsersBookingSerializer(serializers.ModelSerializer):

    room = TinyRoomSerializer()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "experience_date",
            "room",
        )
