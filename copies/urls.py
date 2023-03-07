from django.urls import path
from .views import CopieView


urlpatterns = [
    path("copies/<int:book_id>/", CopieView.as_view()),
]
