from django.shortcuts import render
from .models import ImagenesSala
from .serialziers import ImagenesSalaSerializer
from rest_framework import viewsets

# Create your views here.

class ImagenesSalaViewSet(viewsets.ModelViewSet):
    queryset = ImagenesSala.objects.all()
    serializer_class = ImagenesSalaSerializer
    lookup_field = 'id'