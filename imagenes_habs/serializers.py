from .models import ImagenHabitacion
from rest_framework import serializers

class ImagenHabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenHabitacion
        fields = '__all__'
        read_only_fields = ['id']