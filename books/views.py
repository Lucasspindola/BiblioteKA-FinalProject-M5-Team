from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import CustomBookPermission
from .pagination import CustomBookPagination
from django_filters import rest_framework as filters


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


class FollowView(ListCreateAPIView):
    ...
