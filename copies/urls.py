from django.urls import path
from .views import LoansView


urlpatterns = [
    path("loans/", LoansView.as_view()),
]
