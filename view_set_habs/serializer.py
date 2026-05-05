from rest_framework import serializers
from .models import Habitacion

class HabitacionSerializer(serializers.ModelSerializer):
    tipo_habitacion = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Habitacion
        fields = '__all__'
        read_only_fields = ['id']