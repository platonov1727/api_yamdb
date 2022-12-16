from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserMePatchView, UserViewSet)

router = DefaultRouter()

router.register('users', UserViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r"titles/(?P<title_id>\d+)/reviews",
                ReviewViewSet,
                basename='reviews')
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename='coomments')

urlpatterns = [
    path('v1/users/me/', UserMePatchView.as_view()),
    path('v1/', include(router.urls)),
]
