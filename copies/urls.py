from django.urls import path
from .views import CopieView, LoansView, LoanDetailView, LoanHistoryView


urlpatterns = [
    path("copies/<int:book_id>/", CopieView.as_view()),
    path("books/<int:pk>/loans/", LoansView.as_view()),  # adm
    path("books/<int:pk>/loans/devolution/", LoanDetailView.as_view()),  # adm
    path("users/<int:user_id>/loans/", LoanHistoryView.as_view()),
]
