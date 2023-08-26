from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views


app_name = "auth"

urlpatterns = [
    path("users/", views.UserListAPIView.as_view(), name="users-list"),
    path("users/me", views.ProfileView.as_view(), name="current-user"),
    path("login", views.LoginAPIView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("refresh", TokenRefreshView.as_view(), name="jwt-refresh")
]
