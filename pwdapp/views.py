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





@api_view(['POST'])
def verify_pwd(request):
    mac_address = request.data.get('mac_address')
    id_number = request.data.get('id_number')

    # Check if the MAC address and ID number are provided
    if not mac_address or not id_number:
        return Response({"status": "mac address or id number missing"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if PWD exists in the database
    pwd = PWD.objects.filter(mac_address=mac_address, id_number=id_number).first()

    if pwd:
        serializer = PWDSerializer(pwd)  # Serialize the PWD instance
        return Response({"status": "verified", "pwd_info": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "not verified"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def process_violation(request):
    violation_id = request.data.get('violation_id')
    
    # Get the violation instance or return 404 if not found
    violation = get_object_or_404(TrafficViolation, id=violation_id)
    
    # Call the process_image function directly if you want to process it again
    process_result = process_image(violation)

    if isinstance(process_result, dict) and 'error' in process_result:
        return Response(process_result, status=status.HTTP_400_BAD_REQUEST)

    # Return the updated violation data
    return Response(TrafficViolationSerializer(violation).data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def get_pwd_by_id(request, id_number):
    # Check if a PWD with the provided id_number exists
    exists = PWD.objects.filter(id_number=id_number).exists()

    # Return "yes" if exists, otherwise "no"
    if exists:
        return Response({"yes"}, status=status.HTTP_200_OK)
    else:
        return Response({"no"}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
def upload_violation(request):
    # Check if chat_id and photo are provided in the request data
    chat_id = request.data.get('chat_id')
    photo = request.data.get('photo')

    if not chat_id or not photo:
        return Response({"error": "No chat_id or photo provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Construct the file URL
    image_url = f"https://api.telegram.org/file/bot7995325127:AAE8iqnLoEFovSAMDa9EKEZXVgtAAIQ26fI/{photo}"  # Use your actual BOT token here
    response = requests.get(image_url)

    if response.status_code != 200:
        return Response({"error": "Failed to retrieve image from Telegram"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a file-like object from the response content
    image_file = ContentFile(response.content, name=photo)

    # Save the image to your model
    violation = TrafficViolation(car_image=image_file)  # Ensure your model has the field car_image
    violation.save()

    return Response({"status": "success"}, status=status.HTTP_201_CREATED)

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