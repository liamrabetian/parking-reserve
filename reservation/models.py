from django.db import models
from django.contrib.auth.models import User
import qrcode
import os


class Floor(models.Model):
    floor_number = models.CharField(max_length=2)

    def __str__(self):
        return self.floor_number


class ParkingSlot(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    slot_number = models.CharField(max_length=2)

    def __str__(self):
        return self.slot_number


class Reservation(models.Model):
    start_date = models.DateTimeField(blank=True, null=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enter_date = models.DateTimeField(blank=True, null=True)
    exit_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to="qrcode", blank=True, null=True)

    def __str__(self):
        created_date = str(self.created_date)
        return created_date

    # create a qrcode unique to the reservation object
    def create_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.pk)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{os.getcwd()}/qrcode/{self.pk}.png")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_qrcode()
