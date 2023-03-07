from django.urls import path
from .views import BookDetailView, BookView


urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),
]
