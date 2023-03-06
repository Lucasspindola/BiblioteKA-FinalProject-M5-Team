from django.urls import path
from .views import UserView, UserDetailView, LoginJWTView


urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
    path("users/login/", LoginJWTView.as_view()),
]
