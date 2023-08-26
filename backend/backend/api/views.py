from rest_framework import generics

from backend.api.models import Presentation
from backend.api.serializers import (
    PresentationSerializer,
    ExtendedPresentationSerializer,
)
from backend.api.tasks import process_presentation
from backend.permissions import IsOwner


class PresentationAPIList(generics.ListCreateAPIView):
    queryset = Presentation.objects.all().order_by('-id')
    serializer_class = PresentationSerializer
    filterset_fields = ["creator__id", "result__pptx_status"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PresentationSerializer
        return ExtendedPresentationSerializer

    def post(self, request, *args, **kwargs):
        res = self.create(request, *args, **kwargs)
        process_presentation.delay(res.data["id"])
        return res


class PresentationAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    permission_classes = (IsOwner,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ExtendedPresentationSerializer
        return PresentationSerializer
