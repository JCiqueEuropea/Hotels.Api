from django.db import models

# Create your models here.
class TipoHabitacion(models.Model):
    id_tipo_habitacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    

    def __str__(self):
        return self.nombre