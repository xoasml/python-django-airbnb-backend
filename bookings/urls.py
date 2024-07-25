from django.urls import path
from .views import UsersRoomBooking

urlpatterns = [
    path("@<str:username>/", UsersRoomBooking.as_view()),
]
