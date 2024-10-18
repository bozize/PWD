import re
import binascii
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TrafficViolation
from .utils import process_image  # Import the OCR processing function

@receiver(post_save, sender=TrafficViolation)
def process_violation(sender, instance, created, **kwargs):
    if created:
        # Automatically process the image when a new TrafficViolation is created
        process_image(instance)
