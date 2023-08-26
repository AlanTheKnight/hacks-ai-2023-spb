from rest_framework import serializers

from .utils import verify_telegram_authentication
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for `User` model."""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "id",
            "photo_url",
            "is_active",
            "last_login",
            "date_joined",
            "is_admin",
        ]

        read_only_fields = ["id", "is_active", "username"]


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for authentication data received from Telegram."""

    hash = serializers.CharField()
    auth_date = serializers.IntegerField()
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "photo_url",
            "id",
            "auth_date",
            "hash",
        ]
        extra_kwargs = {
            "hash": {"write_only": True},
            "auth_date": {"write_only": True},
            "id": {"write_only": True},
        }

    def validate(self, data):
        verify_telegram_authentication(data)
        return data

    def create(self, validated_data: dict):
        """Create a new student."""
        user = User.objects.create(
            username=validated_data["username"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            photo_url=validated_data["photo_url"],
            telegram_id=validated_data["id"],
        )
        user.set_password("")
        user.save()
        return user


class TelegramAuthDataSerializer(CreateUserSerializer):
    username = serializers.CharField()

    def validate_username(self, val):
        return val
