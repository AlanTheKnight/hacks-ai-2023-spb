from django.urls import path
from backend.api.views import (
    PresentationAPIList,
    PresentationAPIDetail,
)

app_name = "api"

urlpatterns = [
    path("presentations/", PresentationAPIList.as_view()),
    path("presentations/<int:pk>", PresentationAPIDetail.as_view()),
]
