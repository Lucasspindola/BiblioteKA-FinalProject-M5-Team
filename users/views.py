from .models import User
from .serializers import UserSerializer, CustomJWTSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerUserPermission
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer

    @extend_schema(
        operation_id="api_users_login_create",  # (1) # (2)
        description="Route to login of users. Must be registered to get the expected return.",
        summary="User login",
        tags=["Login"],
        responses={200: TokenObtainPairSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="api_users_create",  # (1) # (2)
        description="Route for creating users and defining their permission level.",
        summary="User create",
        tags=["Users"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerUserPermission]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"

    @extend_schema(
        operation_id="api_users_retrieve",  # (1) # (2)
        description="Route to return data from a single user. Must be admin or owner to be able to do the search.",
        summary="Retrieve data from a user 🔐",
        tags=["Users"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="api_users_partial_update",  # (1) # (2)
        description="Route to update a user's data. Must be admin or the owner to be able to do the request.",
        summary="User data update 🔐",
        tags=["Users"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        operation_id="api_users_destroy",  # (1) # (2)
        description="Route to delete a user's data. Must be admin or the owner to be able to do the request.",
        summary="User data delete 🔐",
        tags=["Users"],
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @extend_schema(
        operation_id="api_users_update",  # (1) # (2)
        description="Route to update a user completely. Must be admin or the owner to be able to do the request.",
        summary="User data update 🔐",
        exclude=True,
        tags=["Users"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
