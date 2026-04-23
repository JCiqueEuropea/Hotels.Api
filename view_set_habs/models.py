from django.db import models
from viewset_tipos_habs.models import TipoHabitacion

# Create your models here.
class Habitacion(models.Model):
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)
    capacidad = models.IntegerField()
    numero_disponibles = models.IntegerField()

    def __str__(self):
        return f'{self.tipo_habitacion} - {self.numero_disponibles} disponibles'
    
    def to_dict(self):
        return {
            'id': self.id,
            'precio_noche': str(self.precio_noche),
            'tipo_habitacion': self.tipo_habitacion.nombre,
            'capacidad': self.capacidad,
            'numero_disponibles': self.numero_disponibles,
        }