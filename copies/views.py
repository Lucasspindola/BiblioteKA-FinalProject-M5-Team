from django.shortcuts import render
from serializers import LoanSerializer
from rest_framework.generics import CreateAPIView
from .models import Loan


# Create your views here.
class LoansView(CreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
