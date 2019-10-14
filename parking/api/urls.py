from django.urls import path
from .views.create_parking import create_parking

urlpatterns = [
    path("create", create_parking, name="create-parking")
]