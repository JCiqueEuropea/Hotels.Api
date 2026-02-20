import uuid
from django.db import models
from .customer import CustomerModel
from .room import RoomModel


class ReservationModel(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, related_name="reservations")
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE, related_name="reservations")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    class Meta:
        db_table = "reservations"
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        indexes = [
            models.Index(fields=["room", "start_date", "end_date", "status"], name="res_room_dates_status_idx"),
        ]
