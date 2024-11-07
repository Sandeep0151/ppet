from django.db import models
from django.contrib.auth.models import User
import uuid
import random
import string


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_number = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forgot_password_token = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username