from django.db import models
from django.utils import timezone
import random


class Appointment(models.Model):
    booking_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    number = models.IntegerField()
    pet = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=200)
    selected_service = models.CharField(max_length=200)
    pet_name = models.CharField(max_length=100, default="", null=True, blank=True)
    pickup_location = models.CharField(max_length=200, default="", null=True, blank=True)
    drop_location = models.CharField(max_length=200, default="", null=True, blank=True)
    instructions = models.TextField(default="", null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    signature_name = models.CharField(max_length=200, default="")
    owner_sign = models.ImageField(default="static/img/arth_sign.png")

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = generate_unique_booking_id()
        super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Appointment #{self.booking_id} - {self.name}"


def generate_unique_booking_id():
    bi = str("PPET")
    random_number = random.randint(10000, 99999)
    booking_id = f"{bi}-{random_number}"
    return booking_id


class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name


