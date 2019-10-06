from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.urls import reverse
import os


class Floor(models.Model):
    floor_number = models.PositiveIntegerField()

    def __str__(self):
        floor_number = str(self.floor_number)
        return floor_number

class ParkingSlot(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    slot_number = models.PositiveIntegerField()

    def __str__(self):
        slot_number = str(self.slot_number)
        return slot_number


class Reservation(models.Model):
    start_date = models.DateTimeField(blank=True, null=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enter_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qrcode', blank=True, null=True)

    def __str__(self):
        created_date = str(self.created_date)
        return created_date


    # def get_absolute_url(self):
    #        return reverse('reserve-parking', args=[str(self.id)])

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
        img.save(f'{os.getcwd()}/qrcode/{self.pk}.png')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_qrcode()