from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import CustomBookPermission
from .pagination import CustomBookPagination
from django_filters import rest_framework as filters
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from .mixins import CustomFollowMixin


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    author = filters.CharFilter(field_name="author", lookup_expr="icontains")


class BookView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    pagination_class = CustomBookPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter


class BookDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FollowView(CustomFollowMixin, CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer