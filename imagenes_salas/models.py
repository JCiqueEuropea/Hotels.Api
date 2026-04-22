from django.db import models
from viewset_salas.models import Sala

# Create your models here.
class ImagenesSala(models.Model):
    url = models.URLField(max_length=500)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='imagenes')

    def __str__(self):
        return self.url