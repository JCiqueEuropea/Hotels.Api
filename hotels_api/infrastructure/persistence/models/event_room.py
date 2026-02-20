import uuid
from django.db import models
from .hotel import HotelModel


class EventRoomModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.ForeignKey(HotelModel, on_delete=models.CASCADE, related_name="event_rooms")
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    hourly_rate_amount = models.DecimalField(max_digits=12, decimal_places=2)
    hourly_rate_currency = models.CharField(max_length=3, default="USD")
    schedule = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "event_rooms"
        verbose_name = "Event Room"
        verbose_name_plural = "Event Rooms"
