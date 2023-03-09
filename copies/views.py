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
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, date


# Create your views here.


class CopieView(CreateCopieMixin, generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    serializer_class = CopieSerializer


class LoansView(CreateLoanMixin, generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    user_queryset = User.objects.all()
    book_queryset = Book.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class LoanDetailView(UpdateLoanMixin, generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    book_queryset = Book.objects.all()
    user_queryset = User.objects.all()
