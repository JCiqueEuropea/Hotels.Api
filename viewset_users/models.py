from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    birth_date = models.DateField(null=True, blank=True)
    is_hotel_manager = models.BooleanField(default=False)
    image_url = models.URLField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username