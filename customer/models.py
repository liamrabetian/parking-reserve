from django.db import models

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=10)
    registration_date = models.DateTimeField(auto_now_add=True)
