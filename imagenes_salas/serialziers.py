from .models import ImagenesSala
from rest_framework import serializers

class ImagenesSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenesSala
        fields = '__all__'
        read_only_fields = ['id']