from django.urls import path
from .views import CopieView, LoansView, LoanDetailView, LoanHistoryView


urlpatterns = [
    path("copies/<int:book_id>/", CopieView.as_view()),
    path("books/loans/<int:pk>/", LoansView.as_view()),  # adm
    path("books/loans/devolution/<int:pk>/", LoanDetailView.as_view()),  # adm
    path("books/loans/history/<int:user_id>/", LoanHistoryView.as_view()),
]
