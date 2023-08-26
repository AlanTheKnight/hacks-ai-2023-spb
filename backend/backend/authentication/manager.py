from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Manager class for `apps.auth.models.User` model."""

    use_in_migrations = True

    def _create_user(self, username, password: str, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password: str, **extra_fields):
        """Create a user with given credentials."""
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password: str, **extra_fields):
        """Create a superuser with given credentials."""
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)
