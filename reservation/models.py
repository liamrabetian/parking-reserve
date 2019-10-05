from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys



class Floor(models.Model):
    floor_number = models.PositiveIntegerField()


class ParkingSlot(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    slot_number = models.PositiveIntegerField()


class Reservation(models.Model):
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enter_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qrcode', blank=True, null=True)


    # def get_absolute_url(self):
    #        return reverse('reserve-parking', args=[str(self.id)])

    # def save(self):
    #     qr = qrcode.QRCode(
    #     version=1,
    #     error_correction=qrcode.constants.ERROR_CORRECT_L,
    #     box_size=10,
    #     border=4,
    #     )
    #     qr.add_data(self.get_absolute_url)
    #     qr.make(fit=True)
    #     img = qr.make_image(fill_color="black", back_color="white")
    #     buffer = BytesIO()
    #     img.save(buffer, format='PNG')
    #     filename = f'events-{self.id}.png'
    #     file_buffer = InMemoryUploadedFile(buffer, 'qrcode', None,
    #                                 'image/png', sys.getsizeof(buffer), None)
    #     self.qr_code.save(filename, file_buffer)