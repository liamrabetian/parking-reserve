from django.db import models
from django.contrib.auth.models import User


CHOICES = {
    ('Y', 'Yes'),
    ('N', 'No')
}


class ParkingLot(models.Model):
    number_of_floors = models.PositiveIntegerField()
    is_lot_available = models.CharField(max_length=1, choices=CHOICES)
    

class Floor(models.Model):
    parking_lot_id = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    number_of_lots = models.PositiveIntegerField()


class ParkingSlot(models.Model):
    floor_id = models.ForeignKey(Floor, on_delete=models.CASCADE)
    slot_number = models.PositiveIntegerField()


class Reservation(models.Model):
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    parking_space_number = models.CharField(max_length=4)
    parking_slot_id = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


