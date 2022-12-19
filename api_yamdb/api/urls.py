from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdminAPI, CategoryViewSet, CommentViewSet, GenreViewSet,
                    RegistrationAPI, ReviewViewSet, TitleViewSet, TokenAPI,
                    UserMePatchView, AdminAPI)

router = DefaultRouter()

router.register('users', AdminAPI)
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
    path('v1/auth/signup/', RegistrationAPI),
    path('v1/auth/token/', TokenAPI.as_view()),
]
