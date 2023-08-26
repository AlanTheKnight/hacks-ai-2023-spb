from django.urls import path
from backend.api.views import (
    PresentationAPIList,
    PresentationAPIDetail,
    ResultAPIDetail,
)

app_name = "api"

urlpatterns = [
    path("presentations/", PresentationAPIList.as_view()),
    path("presentations/<int:pk>", PresentationAPIDetail.as_view()),
    path("result/<int:pk>", ResultAPIDetail.as_view()),
]
