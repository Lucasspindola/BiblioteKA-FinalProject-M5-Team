from django.urls import path
from .views import UserView, UserDetailView, LoginJWTView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
    path("users/login/", LoginJWTView.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "biblioteka/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "biblioteka/docs/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
