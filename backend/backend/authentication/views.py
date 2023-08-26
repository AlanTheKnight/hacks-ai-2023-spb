from django.conf import settings
from rest_framework import generics, permissions, response, status, views, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    RefreshTokenSerializer,
    UserBulkDeleteSerializer,
    UserSerializer,
    TelegramAuthDataSerializer,
    CreateUserSerializer,
    DeliveryManSerializer,
    ManagerSerializer,
)


# from backend.permissions import IsAdminPermission


class ProfileView(generics.RetrieveAPIView):
    """Retrieve current user."""

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Get current user."""
        print("OKKKKK")
        return self.request.user


class UserListAPIView(generics.ListAPIView):
    """List users."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a user."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserBulkDeleteAPIView(generics.DestroyAPIView):
    """
    Delete multiple users.

    Raises:
        Http403Forbidden: If the number of users to delete is greater than 50.
        Http400BadRequest: If the request data is invalid.

    Returns:
        Http204NoContent: If the users were deleted successfully.
    """

    serializer_class = UserBulkDeleteSerializer
    queryset = User.objects.all()

    # permission_classes = [IsAdminPermission]

    def destroy(self, request, *args, **kwargs):
        """Delete multiple users."""
        serializer = UserBulkDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_delete = list(map(int, request.data["ids"].split(",")))
        if len(to_delete) > settings.REST_FRAMEWORK["PAGE_SIZE"]:
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        self.get_queryset().filter(id__in=to_delete).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):
    """Logout users by blacklisting their refresh token."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """Logout the user."""
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise TokenError(e)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class LoginAPIView(views.APIView):
    """APIView for user authentication."""

    def get_user(self, telegram_id: int):
        try:
            return User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return None

    def post(self, request):
        serializer = TelegramAuthDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        telegram_id = serializer.validated_data["id"]
        user = self.get_user(telegram_id)
        if user is None:  # Create a new user
            serializer = CreateUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

        refresh = RefreshToken.for_user(user)
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(response_data, status.HTTP_200_OK)
