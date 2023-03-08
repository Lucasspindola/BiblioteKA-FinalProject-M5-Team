from django.urls import path
from .views import CopieView, LoansView


urlpatterns = [
    path("copies/<int:book_id>/", CopieView.as_view()),
    path("loans/", LoansView.as_view()),
    path("books/loans/<int:pk>/", LoansView.as_view()),
    path("books/loans/devolution/<int:pk>/", LoansView.as_view()),
    path("books/loans/<int:pk>/", LoansView.as_view()),
]
