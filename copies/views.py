from django.shortcuts import render
from rest_framework.views import Request, Response
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
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

# Create your views here.


class CopieView(CreateCopieMixin, generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    serializer_class = CopieSerializer
    lookup_url_kwarg = "book_id"

    @extend_schema(
        operation_id="api_copies_create",  # (1) # (2)
        description="Route to add multiple copies to a book. Admins only.",
        summary="Copies create 🔏",
        tags=["Copies"],
        responses={
            201: OpenApiResponse(
                response="1 copies added to Livro1",
                description="Created",
                examples=[
                    OpenApiExample(
                        "Example 1",
                        value={"detail": "1 copies of 'Livro1' has been added."},
                    )
                ],
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoansView(CreateLoanMixin, generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomLoanPermission]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    user_queryset = User.objects.all()
    book_queryset = Book.objects.all()

    pagination_class = CustomBookPagination
    lookup_url_kwarg = "book_id"

    @extend_schema(
        operation_id="api_books_loans_create",  # (1) # (2)
        description="Route to create a loan of a book. Admins only.",
        summary="Loan creation 🔏",
        tags=["Loans"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoanHistoryView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomLoanHistoryPermission]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    pagination_class = CustomBookPagination
    lookup_url_kwarg = "user_id"

    @extend_schema(
        operation_id="api_users_loans_list",  # (1) # (2)
        description="Route for listing a user's loans. Must be admin or owner to be able to do the search.",
        summary="Loan history 🔐",
        tags=["Loans"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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


class LoanDetailView(UpdateLoanMixin, generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomLoanPermission, IsAuthenticated]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    book_queryset = Book.objects.all()
    user_queryset = User.objects.all()

    lookup_url_kwarg = "book_id"

    @extend_schema(
        operation_id="api_books_loans_devolution_partial_update",  # (1) # (2)
        description="Route to return a book. Admins only.",
        summary="Loan devolution 🔏",
        tags=["Loans"],
        exclude=True,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        operation_id="api_books_loans_devolution_update",  # (1) # (2)
        description="Route to return a book. Admins only.",
        summary="Loan devolution 🔏",
        tags=["Loans"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
