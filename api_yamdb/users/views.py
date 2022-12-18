from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, filters, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, TokenSerializer
from .permissions import IsAdmin
from api_yamdb.settings import DEFAULT_FROM_EMAIL


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
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = request.data.get('confirmation_code')
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {"token": str(refresh.access_token)},
                    status=status.HTTP_200_OK
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
