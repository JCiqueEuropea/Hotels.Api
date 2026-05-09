from django.db import models
from viewset_salas.models import Sala
from viewset_users.models import User

# Create your models here.
class ReservaSala(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Reserva de {self.usuario.username} para la sala {self.sala.id} desde {self.fecha_inicio} hasta {self.fecha_fin}"

    def to_dict(self):
        return {
            'id': self.id,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'sala': self.sala.id,
            'usuario': self.usuario.id,
            'confirmed': self.confirmed,
        }