from django.db import models
from view_set_habs.models import Habitacion
from viewset_users.models import User

# Create your models here.
class ReservaHabitacion(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva de {self.usuario.username} para la habitación {self.habitacion.numero} desde {self.fecha_inicio} hasta {self.fecha_fin}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'habitacion': self.habitacion.id,
            'usuario': self.usuario.id
        }