from django.urls import path
from .views import BookDetailView, BookView, FollowView


urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),
    path("users/follow/<int:pk>", FollowView.as_view()),
]
