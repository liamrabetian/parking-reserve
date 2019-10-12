from django.db import models


class Floor(models.Model):
    floor_number = models.CharField(max_length=2)

    def __str__(self):
        return self.floor_number


class ParkingSlot(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    slot_number = models.CharField(max_length=2)

    def __str__(self):
        return self.slot_number
