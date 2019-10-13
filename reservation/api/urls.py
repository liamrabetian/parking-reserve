from django.urls import path
from reservation.api.views.reserve import reserve_parking
from reservation.api.views.available_parkings import available_parkings
from reservation.api.views.exit_parking import exit_parking
from reservation.api.views.create_parking import create_parking
from reservation.api.views.cancel_reserve import cancel_reserve
from reservation.api.views.active_reservations import active_reservations
from reservation.api.views.enter_parking import enter_parking
from reservation.api.views.user_active_reservations import user_active_reservations


urlpatterns = [
    path("reserve", reserve_parking, name="reserve-parking"),
    path("available_parkings", available_parkings, name="available-parkings"),
    path("exit", exit_parking, name="exit"),
    path("create", create_parking, name="create-parking"),
    path("cancel", cancel_reserve, name="cancel"),
    path("active_reservations", active_reservations,
         name="active-reservations"),
    path("enter_parking", enter_parking, name="enter-parking"),
    path("user_active_reservations", user_active_reservations, name="user-active-reservations")
]
