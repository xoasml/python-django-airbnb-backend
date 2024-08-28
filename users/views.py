from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.exceptions import NotFound

import jwt
import requests


from . import serializers
from .models import User


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):

    def post(self, request):
        # password = request.data.get("password")
        # if not password:
        #     raise ParseError
        # serializer = serializers.PrivateUserSerializer(data=request.data)
        # if serializer.is_valid():
        #     user = serializer.save()
        #     user.set_password(password)
        #     user.save()
        #     serializer = serializers.PrivateUserSerializer(user)
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors)
        return Response(status=status.HTTP_200_OK)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("유저를 확인 해주세요")

        serializer = serializers.PublicUserSerializer(user)
        return Response(serializer.data)


class SignUp(APIView):

    def post(self, request):

        try:
            User.objects.get(email=request.data.get("email"))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "이미 존재하는 email 입니다."},
            )
        except User.DoesNotExist:
            user = User.objects.create(
                name=request.data.get("name"),
                email=request.data.get("email"),
                username=request.data.get("username"),
            )

            user.set_password(request.data.get("password"))
            user.save()

            return Response(status=status.HTTP_200_OK, data={"ok": "회원가입 성공"})


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            print("ok")
            return Response({"ok": "Welcome"})
        else:
            print("nogood")
            return Response(
                {"error": "wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogOut(APIView):

    def post(self, request):
        logout(request)
        return Response({"ok": "bye"})


class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GithubLogIn(APIView):

    def post(self, request):
        try:
            code = request.data.get("code")

            # token 발급 받기
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=Ov23lir3uFzYk7Fyu6fl&client_secret={settings.SECRET_GITHUB}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")

            # token 이용해서 유저 데이터 받아오기
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()

            # token 이용해서 유저 이메일 받아오기
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()

            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_emails[0]["email"],
                    name=user_data.get("name"),
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KaKaoLogin(APIView):

    def post(self, request):
        try:
            code = request.data.get("code")

            access_token = requests.post(
                url="https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "4e6252a4154f2982cadd9b0ec684cbe0",
                    "redirect_uri": "http://127.0.0.1:3001/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")

            user_data = requests.post(
                url="https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")

            test_mail = str(user_data.get("id")) + "@test.com"
            print(test_mail)

            try:

                user = User.objects.get(email=test_mail)
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=test_mail,
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                # 패스워드 미사용
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
