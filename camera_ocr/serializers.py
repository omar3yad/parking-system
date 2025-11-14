from rest_framework import serializers
from .models import Camera, OCRLog
from parking.serializers import ParkingSlotSerializer

class CameraSerializer(serializers.ModelSerializer):
    monitoring_slots = ParkingSlotSerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = ['id', 'camera_name', 'location', 'monitoring_slots', 'created_at']

class OCRLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRLog
        fields = ['id', 'camera', 'slot', 'plate_number', 'detected_at']
