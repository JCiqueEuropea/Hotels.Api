import uuid
from django.db import models
from .hotel import HotelModel


class RoomModel(models.Model):
    ROOM_TYPE_CHOICES = (
        ("SINGLE", "SINGLE"),
        ("DOUBLE", "DOUBLE"),
        ("SUITE", "SUITE"),
        ("DELUXE", "DELUXE"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.ForeignKey(HotelModel, on_delete=models.CASCADE, related_name="rooms")
    number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    price_amount = models.DecimalField(max_digits=12, decimal_places=2)
    price_currency = models.CharField(max_length=3, default="USD")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "rooms"
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        unique_together = ("hotel", "number")
