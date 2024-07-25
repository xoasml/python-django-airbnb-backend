from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Review
from .serializers import UsersRoomReviewSerializer


class UsersRoomReview(APIView):

    def get_object(self, username):
        try:
            return Review.objects.filter(
                user__username=username,
                room__isnull=False,
            )
        except Review.DoesNotExist:
            return NotFound

    def get(self, reqeust, username):
        review = self.get_object(username=username)
        serializer = UsersRoomReviewSerializer(review, many=True)

        return Response(serializer.data)
