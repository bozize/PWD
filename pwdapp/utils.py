# utils.py
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from django.conf import settings
import re
from .models import RoadUser

# this handles the the image processing using azure computer vission
def get_computervision_client():
    endpoint = settings.AZURE_COMPUTER_VISION_ENDPOINT
    key = settings.AZURE_COMPUTER_VISION_KEY
    credentials = CognitiveServicesCredentials(key)
    return ComputerVisionClient(endpoint, credentials)

def process_image(violation):
    try:
        computervision_client = get_computervision_client()
        car_image_path = violation.car_image.path
        
        with open(car_image_path, "rb") as image_stream:
            ocr_result = computervision_client.read_in_stream(image_stream, raw=True)
        
        operation_location_remote = ocr_result.headers["Operation-Location"]
        operation_id = operation_location_remote.split("/")[-1]

        while True:
            result = computervision_client.get_read_result(operation_id)
            if result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                break
        
        if result.status == OperationStatusCodes.succeeded:
            read_results = result.analyze_result.read_results
            number_plate = None
            
            for text_result in read_results:
                for line in text_result.lines:
                    print("Detected text:", line.text)
                    matches = re.findall(r'([A-Za-z]{3})\W*([0-9]{3})\W*([A-Za-z]?)', line.text)
                    if matches:
                        number_plate = ''.join(matches[0])
                        break
                if number_plate:
                    break
            
            if number_plate:
                if len(number_plate) != 7:
                    return {"error": "Invalid number plate format"}
                
                violation.number_plate = number_plate
                road_user_exists = RoadUser.objects.filter(number_plate=number_plate).exists()
                violation.verified = road_user_exists
                violation.blacklisted = road_user_exists
                
                violation.save()
                return {"status": "processed", "number_plate": number_plate}
            else:
                return {"error": "No valid number plate detected"}
    
    except FileNotFoundError:
        return {"error": "Image file not found"}
    except Exception as e:
        return {"error": str(e)}