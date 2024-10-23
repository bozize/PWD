from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import PWD, TrafficViolation, RoadUser
from .serializers import PWDSerializer, TrafficViolationSerializer
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes 
from msrest.authentication import CognitiveServicesCredentials
import binascii
from PIL import Image
import re
from .utils import process_image
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile








# this view processes image detection for violations
@api_view(['POST'])
def process_violation(request):
    violation_id = request.data.get('violation_id')
    
    
    violation = get_object_or_404(TrafficViolation, id=violation_id)
    
    
    process_result = process_image(violation)

    if isinstance(process_result, dict) and 'error' in process_result:
        return Response(process_result, status=status.HTTP_400_BAD_REQUEST)

   
    return Response(TrafficViolationSerializer(violation).data, status=status.HTTP_200_OK)
    
# this view verifies pwd existence
@api_view(['GET'])
def get_pwd_by_mac(request, mac_address):
    
    exists = PWD.objects.filter(mac_address=mac_address).exists()

    
    if exists:
        return Response({"message": "yes"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "no"}, status=status.HTTP_404_NOT_FOUND)





import logging



"""
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        # Log incoming data
        logger.debug("Incoming data: %s", request.body)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %s", e)
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Check for photo in the message
        if 'message' in data:
            message = data['message']
            if 'photo' in message:
                file_id = message['photo'][-1]['file_id']
                bot_token = '7995325127:AAE8iqnLoEFovSAMDa9EKEZXVgtAAIQ26fI'
                file_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"

                # Get file info from Telegram
                file_info = requests.get(file_url).json()
                if not file_info.get('ok'):
                    logger.error("Failed to get file info: %s", file_info)
                    return JsonResponse({"error": "Failed to get file info"}, status=400)

                file_path = file_info['result']['file_path']
                image_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

                # Download the image
                image_data = requests.get(image_url).content

                # Send the image to the Django backend
                files = {'car_image': ('car_image.jpg', image_data, 'image/jpeg')}
                django_api_url = 'https://39f7-197-232-150-13.ngrok-free.app/api/upload-violation/'
                response = requests.post(django_api_url, files=files)

                if response.status_code == 201:
                    return JsonResponse({"status": "Image uploaded successfully"}, status=200)
                else:
                    logger.error("Failed to upload image: %s", response.content)
                    return JsonResponse({"error": "Failed to upload image"}, status=400)

            # Handle messages sent by the bot
            if 'from' in message and message['from'].get('is_bot', False):
                logger.info("Received a message from the bot: %s", message.get('text', ''))
                # You can perform additional actions here
                return JsonResponse({"status": "Bot message processed"}, status=200)

        logger.debug("No image found in the message")
        return JsonResponse({"status": "No image found in the message"}, status=200)

    logger.debug("Invalid request method: %s", request.method)
    return JsonResponse({"status": "Invalid request"}, status=400) """