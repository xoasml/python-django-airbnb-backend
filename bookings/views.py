from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import UsersBookingSerializer
from .models import Booking


class UsersRoomBooking(APIView):

    def get(self, reqeust, username):
        try:
            bookings = Booking.objects.filter(user__username=username)
            serializer = UsersBookingSerializer(bookings, many=True)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            raise NotFound
