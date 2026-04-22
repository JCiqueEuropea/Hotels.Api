from rest_framework import serializers
from .models import Sala

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'
        read_only_fields = ['id']