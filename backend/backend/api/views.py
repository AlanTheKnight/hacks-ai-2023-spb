from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from backend.api.models import Presentation
from backend.api.serializers import PresentationSerializer
from backend.permissions import IsOwner


class PresentationAPIList(generics.ListCreateAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    permission_classes = (IsAdminUser,)


class PresentationAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    permission_classes = (IsOwner, IsAdminUser,)
