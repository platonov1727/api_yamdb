from django.urls import path

from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router = SimpleRouter()

router.register(r'titles', TitleViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
