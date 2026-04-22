from django.shortcuts import render
from rest_framework import viewsets
from .models import Sala
from .serializers import SalaSerializer

# Create your views here.
class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    lookup_field = 'id'