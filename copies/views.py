from django.shortcuts import render
from rest_framework.views import APIView, status, Response
from serializers import CopieLoanSerializer
# Create your views here.
class LoansView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        """
        Emprestimo
        """
        serializer = CopieLoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)