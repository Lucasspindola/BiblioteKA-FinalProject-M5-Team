from django.shortcuts import render
from rest_framework.views import Request, Response, status
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CopieSerializer, LoanSerializer
from .mixins import CreateCopieMixin, CreateLoanMixin, UpdateLoanMixin
from books.permissions import CustomBookPermission
from .models import Loan
from users.models import User
from books.models import Book
from .permissions import CustomLoanPermission, CustomLoanHistoryPermission
from rest_framework.permissions import IsAuthenticated
from books.pagination import CustomBookPagination
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

# Create your views here.


class CopieView(CreateCopieMixin, generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    serializer_class = CopieSerializer


class LoansView(CreateLoanMixin, generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomLoanPermission]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    user_queryset = User.objects.all()
    book_queryset = Book.objects.all()

    pagination_class = CustomBookPagination


class LoanHistoryView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomLoanHistoryPermission]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    pagination_class = CustomBookPagination

    def list(self, request: Request, *args, **kwargs):
        user_obj = get_object_or_404(User, pk=kwargs["user_id"])
        self.check_object_permissions(request, user_obj)
        queryset = self.get_queryset().filter(user=user_obj)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LoanDetailView(UpdateLoanMixin, generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomLoanPermission, IsAuthenticated]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    book_queryset = Book.objects.all()
    user_queryset = User.objects.all()
