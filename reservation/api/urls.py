from django.urls import path
from reservation.api.views.reserve import reserve_parking
from reservation.api.views.available_parkings import available_parkings
from reservation.api.views.exit_parking import exit_parking
from reservation.api.views.create_parking import create_parking
from reservation.api.views.cancel_reserve import cancel_reserve


urlpatterns = [
    path('reserve', reserve_parking, name='reserve-parking'),
    path('available_parkings', available_parkings, name='available-parkings'),
    path('exit', exit_parking, name='exit'),
    path('create', create_parking, name='create-parking'),
    path('cancel', cancel_reserve, name='cancel')
]
