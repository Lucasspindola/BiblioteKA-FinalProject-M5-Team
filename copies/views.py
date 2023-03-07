from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CopieSerializer, LoanSerializer
from .mixins import CreateCopieMixin
from books.permissions import CustomBookPermission
from .models import Loan

# Create your views here.


class CopieView(CreateCopieMixin, CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermission]

    serializer_class = CopieSerializer


class LoansView(CreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
