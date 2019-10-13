from django.urls import path
from .views.user_register import register
from .views.user_logout import user_logout
from .views.user_login import user_login
from .views.admin_register import admin_register


urlpatterns = [
    path('register', register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('admin_register', admin_register, name='admin-register')
]
