from rest_framework import serializers
from .models import SupportConsultation

class SupportConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportConsultation
        fields = '__all__'


class KeySerializer(serializers.Serializer):
    key = serializers.CharField(
        label="Token",
        required=True,
    )
    class Meta:
        fields = ('key',)