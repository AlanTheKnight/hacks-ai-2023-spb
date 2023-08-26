from rest_framework import serializers

from backend.api.models import Presentation, Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"
        read_only_fields = (
            "name_status",
            "logo_status",
            "pptx_status",
            "pptx_data",
            "pptx",
            "presentation",
        )


class PresentationSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # result = ResultSerializer(required=True)

    class Meta:
        model = Presentation
        fields = "__all__"

    def create(self, validated_data):
        # result_data = validated_data.pop('result')
        presentation = Presentation.objects.create(**validated_data)
        result_data = {"presentation": presentation}
        result = ResultSerializer.create(ResultSerializer(), result_data)
        return presentation
