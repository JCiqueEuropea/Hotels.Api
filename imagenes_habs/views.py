from django.shortcuts import render
from rest_framework import viewsets
from .models import ImagenHabitacion
from .serializers import ImagenHabitacionSerializer

# Create your views here.
class ImagenHabitacionViewSet(viewsets.ModelViewSet):
    queryset = ImagenHabitacion.objects.all()
    serializer_class = ImagenHabitacionSerializer
    lookup_field = 'id'