import uuid
from django.db import models


class HotelModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)

    class Meta:
        db_table = "hotels"
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"
