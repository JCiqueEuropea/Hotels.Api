from django.shortcuts import render
from rest_framework import viewsets
from .models import Sala
from .serializers import SalaSerializer
from rest_framework.decorators import action
from imagenes_salas.models import ImagenesSala
from imagenes_salas.serialziers import ImagenesSalaSerializer
from rest_framework.response import Response

# Create your views here.
class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['get'], url_path='imagenes')
    def images(self, request, id=None):
        imagenes = ImagenesSala.objects.filter(sala_id=id)
        serializer = ImagenesSalaSerializer(imagenes, many=True)
        return Response(serializer.data)