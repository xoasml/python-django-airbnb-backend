from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import Perk, Experience
from .serializers import (
    PerkSerializer,
    ExperienceListSerializer,
    CreateExperienceSerializer,
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
