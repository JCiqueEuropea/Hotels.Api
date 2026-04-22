from django.db import models
from view_set_habs.models import Habitacion

# Create your models here.
class ImagenHabitacion(models.Model):
    
    url = models.URLField(max_length=500)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='imagenes')

    def __str__(self):
        return self.url
