from django.urls import path
from .views.create_parking import create_parking
from .views.add_slot import add_slot


urlpatterns = [
    path("create", create_parking, name="create-parking"),
    path("add_slot", add_slot, name="add-slot")
]
