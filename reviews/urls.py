from django.urls import path
from .views import UsersRoomReview

urlpatterns = [
    path("@<str:username>", UsersRoomReview.as_view()),
]
