from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerUserPermission

class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerUserPermission]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    