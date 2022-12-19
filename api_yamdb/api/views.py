from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from titles.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitlesFilter
from .permissions import IsAdmin, IsAdminOrReadOnly, IsStuffOrAuthor
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TokenSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitlesFilter
    permission_classes = (IsAdminOrReadOnly, )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (IsAdmin, )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    # permission_classes = (IsStuffOrAuthor, )


class AdminAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )


class UserMePatchView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response('Вы не авторизованы',
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response('Вы не авторизованы',
                        status=status.HTTP_401_UNAUTHORIZED)


# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStuffOrAuthor, )
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Title, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, title_id=review.id)

    def get_queryset(self):
        review = get_object_or_404(Title, pk=self.kwargs.get("post_id"))
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=["rating"])


class RegistrationAPI(APIView):
    """Аутентификация через верификацию email"""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User,
                                     username=serializer.data['username'])
            confirmation_code = default_token_generator.make_token(user)
            send_mail('Подтверждение регистрации',
                      f'Подтвердите ваш e-mail: {confirmation_code}',
                      DEFAULT_FROM_EMAIL,
                      serializer.data[['email']],
                      fail_silently=False)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TokenAPI(APIView):
    permission_classes = (AllowAny, )
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = request.data.get('confirmation_code')
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                refresh = RefreshToken.for_user(user)
                return Response({"token": str(refresh.access_token)},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
