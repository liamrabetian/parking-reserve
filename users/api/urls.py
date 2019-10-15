from django.urls import path
from .views.user_register import register
from .views.user_logout import user_logout
from .views.user_login import user_login
from .views.admin_register import admin_register
from jwt_auth import views as jwt_auth_views


urlpatterns = [
    path('register', register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('admin_register', admin_register, name='admin-register'),
    path("token_auth/", jwt_auth_views.jwt_token, name="jwt-token"),
    path("token_refresh/", jwt_auth_views.refresh_jwt_token, name="refresh-token")
]
