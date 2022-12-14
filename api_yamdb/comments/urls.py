from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, CommentViewSet

router_v1 = DefaultRouter()

router_v1.register(r"titles/(?P<title_id>\d+)/reviews",
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename='coomments')

urlpatterns = [path('', include(router_v1.urls))]
