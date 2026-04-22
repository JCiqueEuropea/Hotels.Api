from .serializer import HabitacionSerializer
from .models import Habitacion
from rest_framework import viewsets


# Create your views here.
class HabitacionViewSet(viewsets.ModelViewSet):
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer
    lookup_field = 'id'