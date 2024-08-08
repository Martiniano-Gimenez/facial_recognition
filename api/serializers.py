from rest_framework import serializers
from .models import ReferenceImage

class ReferenceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceImage
        fields = ('id', 'name', 'image', 'uploaded_at')
