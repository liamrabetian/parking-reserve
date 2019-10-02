from django.urls import path
from customer.api.views.create_customer import UserCreate

urlpatterns = [
    path('', UserCreate.as_view(), name='user-create')
]