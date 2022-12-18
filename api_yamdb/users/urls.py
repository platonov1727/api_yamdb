from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AdminAPI, RegistrationAPI, TokenAPI


router = DefaultRouter()
router.register('v1/users', AdminAPI)
urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/signup/', RegistrationAPI.as_view()),
    path('v1/auth/token/', TokenAPI.as_view()),
]
