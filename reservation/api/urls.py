from django.urls import path
from reservation.api.views.reserve import reserve_parking
from reservation.api.views.available_parking_lot import get_available_parking_lots

urlpatterns = [
    path('', reserve_parking, name='reserve-view'),
    path('available_parking_lots', get_available_parking_lots, name='parking-view'),

]
