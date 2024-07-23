from rest_framework import serializers
from .models import Booking


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

    def validate_check_in(attrs, value):
        return value

class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests"
        )
