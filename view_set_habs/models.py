from django.db import models


# Create your models here.
class Habitacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    numero_disponibles = models.IntegerField()

    def __str__(self):
        return f'{self.nombre} - {self.numero_disponibles} disponibles'
    
    def to_dict(self):
        return {
            'id': self.id,
            'precio_noche': str(self.precio_noche),
            'tipo_habitacion': self.tipo_habitacion.nombre,
            'capacidad': self.capacidad,
            'numero_disponibles': self.numero_disponibles,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
        }