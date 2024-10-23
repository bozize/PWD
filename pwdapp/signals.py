import re
import binascii
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TrafficViolation
from .utils import process_image

@receiver(post_save, sender=TrafficViolation)
def process_violation(sender, instance, created, **kwargs):
    if created:
        process_image(instance)
