# core/models.py
from django.db import models



class PWD(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    mac_address = models.CharField(max_length=17, unique=True)  # Store as a string
    id_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class TrafficViolation(models.Model):
    car_image = models.ImageField(upload_to='violations/')
    number_plate = models.CharField(max_length=10, blank=True, null=True)
    verified = models.BooleanField(default=False)
    blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return f"Violation for {self.number_plate or 'Unknown'}"
    


class RoadUser(models.Model):
    name = models.CharField(max_length=100)
    number_plate = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} - {self.number_plate}"
