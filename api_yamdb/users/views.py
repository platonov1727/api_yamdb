from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .models import User
from .serializers import UserSerializer, TokenSerializer


class RegistrationAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User, username=serializer.data['username'])
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Подтверждение регистрации',
                f'Подтвердите ваш e-mail: {confirmation_code}',
                DEFAULT_FROM_EMAIL,
                serializer.data['email'],
                fail_silently=False
            )
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TokenAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User, username=serializer.data['username'])
            if default_token_generator.check_token(user, serializer.data['confirmation_code']):
                return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
