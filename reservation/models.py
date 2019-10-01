from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    parking_space_number = models.CharField(max_length=4)
    is_parking_available = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

