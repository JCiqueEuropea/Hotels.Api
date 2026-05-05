from django.db import models
from viewset_tipos_habs.models import TipoHabitacion


# Create your models here.
class Habitacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    numero_disponibles = models.IntegerField()
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} - {self.numero_disponibles} disponibles'
    
    def to_dict(self):
        return {
            'id': self.id,
            'precio_noche': str(self.precio_noche),
            'tipo_habitacion': self.tipo_habitacion.nombre if self.tipo_habitacion else None,
            'capacidad': self.capacidad,
            'numero_disponibles': self.numero_disponibles,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            
        }