from rest_framework import viewsets
from .models import TipoHabitacion
from .serializer import TipoHabitacionSerializer

# Create your views here.
class TipoHabitacionViewSet(viewsets.ModelViewSet):
    queryset = TipoHabitacion.objects.all()
    serializer_class = TipoHabitacionSerializer
    lookup_field = 'id_tipo_habitacion'