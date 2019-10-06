from django.contrib import admin
from reservation.models import Reservation, Floor, ParkingSlot


admin.site.register(Reservation)
admin.site.register(Floor)
admin.site.register(ParkingSlot)