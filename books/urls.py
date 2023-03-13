from django.urls import path
from .views import BookDetailView, BookView, FollowView, DestroyFollowView


urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),
    path("books/<int:pk>/follow/", FollowView.as_view()),
    path("books/<int:pk>/unfollow/", DestroyFollowView.as_view()),
]
