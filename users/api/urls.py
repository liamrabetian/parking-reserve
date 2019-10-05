from django.urls import path
from .views.register_login import register, user_login, user_logout

urlpatterns = [
    path('register', register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout')
]