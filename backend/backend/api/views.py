from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from backend.api.models import Presentation
from backend.api.serializers import PresentationSerializer
from backend.api.tasks import process_presentation
from backend.permissions import IsOwner


class PresentationAPIList(generics.ListCreateAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        res = self.create(request, *args, **kwargs)
        process_presentation.delay(res.data["id"])
        return res


class PresentationAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    permission_classes = (IsOwner, IsAdminUser,)
