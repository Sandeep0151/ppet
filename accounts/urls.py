from .views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("logout/", logout_page, name="logout"),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', reset_password, name='reset_password'),
]

