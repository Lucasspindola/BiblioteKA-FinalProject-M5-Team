from django.urls import path
from .views import BookDetailView, BookView, FollowView, DestroyFollowView


urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/<int:book_id>/", BookDetailView.as_view()),
    path("books/<int:book_id>/follow/", FollowView.as_view()),
    path("books/<int:book_id>/unfollow/", DestroyFollowView.as_view()),
]
