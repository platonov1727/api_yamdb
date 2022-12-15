from django.urls import path

from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import TitleViewSet, GenreViewSet, CategoryViewSet, CommentViewSet, ReviewViewSet

router = DefaultRouter()

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
    path('v1/', include(router.urls)),
]
