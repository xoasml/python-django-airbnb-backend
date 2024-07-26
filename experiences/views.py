from django.db import transaction
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from categories.models import Category
from bookings.models import Booking
from bookings.serializers import (
    PublicBookingSerializer,
    CreateExperiencesBookingSerializer,
)

from .models import Perk, Experience
from .serializers import (
    PerkSerializer,
    ExperienceListSerializer,
    CreateExperienceSerializer,
    DetailExperienceSerializer,
    TinyPerkSerializer,
)


class Perks(APIView):

    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experience = Experience.objects.all()
        serializer = ExperienceListSerializer(
            experience,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateExperienceSerializer(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():
            experience = serializer.save(host=request.user)
            serializer = CreateExperienceSerializer(experience)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = DetailExperienceSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = DetailExperienceSerializer(
            experience,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            if transaction.atomic():
                experience = serializer.save()
                if request.data.get("category"):
                    try:
                        category = Category.objects.get(pk=request.data.get("category"))
                    except Category.DoesNotExist:
                        raise NotFound("그런 category 없어요")

                    if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("Is not experience category")

                    experience = serializer.save(category=category)

                if request.data.get("perks"):
                    try:
                        perks = []
                        for perk in request.data.get("perks"):
                            perks.append(Perk.objects.get(pk=perk))
                    except Perk.DoesNotExist:
                        raise NotFound("그런 perks 없어요")

                    experience = serializer.save(perks=perks)

                serializer = DetailExperienceSerializer(experience)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk=pk)
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperiencesPerks(APIView):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound("Experience 가 없어요")

    def get(self, request, pk):

        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        experience = self.get_object(pk)
        perks = experience.perks.all()[start:end]
        serializer = TinyPerkSerializer(perks, many=True)
        return Response(serializer.data)


class ExperienceBookings(APIView):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound("존재 하지 않는 Experience 입니다.")

    def get(self, request, pk):
        experience = self.get_object(pk)
        bookings = experience.bookings.all()

        if bookings.exists():
            serializer = PublicBookingSerializer(bookings, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = CreateExperiencesBookingSerializer(data=request.data)

        if serializer.is_valid():

            bookings = serializer.save(
                experience=experience,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                user_id=request.user.pk,
            )
            serializer = PublicBookingSerializer(bookings)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


# class ExperiencesBooking
