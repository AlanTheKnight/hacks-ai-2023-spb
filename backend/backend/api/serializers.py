from rest_framework import serializers

from backend.api.models import Presentation


class PresentationSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Presentation
        fields = '__all__'
