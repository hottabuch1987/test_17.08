import time
import random
import string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth import get_user_model

from .serializers import UserSerializer


class SendAuthCode(APIView):
    """Авторизация по номеру телефона"""
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user, created = get_user_model().objects.get_or_create(phone_number=phone_number)

        if created:
            user.invite_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
            user.auth_code = ''.join(random.choice(string.digits) for _ in range(4))
            if password:
                user.set_password(password)  # Установка пароля
            user.save()
            time.sleep(1)
            return Response({"message": "Пользователь создан. Код авторизации отправлен.", "auth_code": user.auth_code,
                             "invite_code": user.invite_code}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Пользователь с таким номером телефона уже существует."},
                            status=status.HTTP_400_BAD_REQUEST)


class CheckAuthCode(APIView):
    """Проверка кода"""
    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')
        user = User.objects.get(phone_number=phone_number)
        if user.auth_code == auth_code:
            return Response({"message": "Код авторизации правильный."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Неверный код авторизации."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    """Профиль пользователя"""

    def get(self, request, phone_number):
        user = User.objects.get(phone_number=phone_number)
        serializer = UserSerializer(user)

        invited_users = User.objects.filter(invite_code=user.invite_code)
        invite_codes = [u.phone_number for u in invited_users]

        serializer.data['invited_users'] = invite_codes

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, phone_number):
        user = User.objects.get(phone_number=phone_number)
        try:
            invite_code = request.data.get('invite_code')
            invited_user = User.objects.get(invite_code=invite_code)

            if user.has_used_invite:
                return Response({"message": "Вы уже использовали код приглашения."}, status=status.HTTP_400_BAD_REQUEST)

            if invited_user.has_used_invite:
                return Response({"message": "Пользователь с данным кодом приглашения уже активировал свой профиль."},
                                status=status.HTTP_400_BAD_REQUEST)

            user.has_used_invite = True
            user.save()

            return Response({"message": "Пригласительный код активирован."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "Неверный код приглашения."}, status=status.HTTP_400_BAD_REQUEST)
