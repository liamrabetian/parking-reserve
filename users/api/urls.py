from django.urls import path
from .views.register_login import register, user_login

urlpatterns = [
    path('register', register, name='register'),
    path('login', user_login, name='login')
]