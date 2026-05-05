from .serializer import HabitacionSerializer
from .models import Habitacion
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from imagenes_habs.models import ImagenHabitacion
from imagenes_habs.serializers import ImagenHabitacionSerializer


# Create your views here.
class HabitacionViewSet(viewsets.ModelViewSet):
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer
    lookup_field = 'id'


    @action(detail=True, methods=['get'], url_path='imagenes')
    def images(self, request, id=None):
        imagenes = ImagenHabitacion.objects.filter(habitacion_id=id)
        serializer = ImagenHabitacionSerializer(imagenes, many=True)
        return Response(serializer.data)