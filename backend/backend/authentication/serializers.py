from rest_framework import serializers

from .utils import UserTypes, verify_telegram_authentication
from .models import User

from backend.apps.authentication.models import DeliveryMan, Manager


class DeliveryManSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMan
        fields = ["status"]


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMan
        fields = ["kitchen_id"]



class UserSerializer(serializers.ModelSerializer):
    """Serializer for `User` model."""
    options_manager = ManagerSerializer()
    options_deliveryman = DeliveryManSerializer()

    class Meta:
        model = User
        fields = [
            "account_type", "first_name", "last_name",
            "username", "id", "photo_url", "is_active",
            "last_login", "date_joined", "is_admin",
            "options_manager", "options_deliveryman"
        ]

        read_only_fields = [
            "id", "account_type", "is_active", "username"
        ]


class UserBulkDeleteSerializer(serializers.Serializer):
    ids = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for authentication data received from Telegram."""

    hash = serializers.CharField()
    auth_date = serializers.IntegerField()
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",
                  "photo_url", "id", "auth_date", "hash"]
        extra_kwargs = {"hash": {"write_only": True}, "auth_date": {
            "write_only": True}, "id": {"write_only": True}}

    def validate(self, data):
        verify_telegram_authentication(data)
        return data

    def create(self, validated_data: dict):
        """Create a new student."""
        user = User.objects.create(
            account_type=UserTypes.COURIER.value,
            username=validated_data["username"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            photo_url=validated_data["photo_url"],
            telegram_id=validated_data["id"]
        )
        user.set_password("")
        user.save()
        return user


class TelegramAuthDataSerializer(CreateUserSerializer):
    username = serializers.CharField()

    def validate_username(self, val):
        return val


