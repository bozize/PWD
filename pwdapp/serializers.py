from rest_framework import serializers
from .models import PWD, TrafficViolation


from .models import RoadUser

class RoadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadUser
        fields = ['id', 'name', 'number_plate', 'phone_number']

class PWDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PWD
        fields = ['id', 'name', 'phone_number', 'mac_address', 'id_number']

class TrafficViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolation
        fields = ['id', 'car_image', 'number_plate', 'verified', 'blacklisted']