from django.urls import path

from .views import RegistrationAPI, TokenAPI

urlpatterns = [
    path('signup/', RegistrationAPI.as_view()),
    path('token/', TokenAPI.as_view())
]
