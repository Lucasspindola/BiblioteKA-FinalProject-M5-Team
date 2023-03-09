from django.urls import path
from .views import CopieView, LoansView, LoanDetailView


urlpatterns = [
    path("copies/<int:book_id>/", CopieView.as_view()),
    path("books/loans/<int:pk>/", LoansView.as_view()),
    path("books/loans/devolution/<int:pk>/", LoanDetailView.as_view()),
    path("books/loans/history/<int:pk>/", LoansView.as_view()),
]
