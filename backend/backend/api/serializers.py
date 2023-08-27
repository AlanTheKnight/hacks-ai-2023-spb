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
        )


class ExtendedPresentationSerializer(serializers.ModelSerializer):
    result = ResultSerializer()

    class Meta:
        model = Presentation
        fields = "__all__"


class PresentationSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    name = serializers.CharField(required=False)
    logo = serializers.ImageField(required=False)

    class Meta:
        model = Presentation
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        results_kwargs = {}
        if "name" in validated_data:
            results_kwargs["name"] = validated_data.pop("name")
        if "logo" in validated_data:
            results_kwargs["logo"] = validated_data.pop("logo")
        presentation = Presentation.objects.create(**validated_data)
        Result.objects.create(presentation=presentation, **results_kwargs)
        return presentation
