from django.db import models
from parking.models import ParkingSlot

class Camera(models.Model):
    camera_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    monitoring_slots = models.ManyToManyField(ParkingSlot, related_name='cameras')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.camera_name} at {self.location}"

class OCRLog(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='ocr_logs')
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE, related_name='ocr_logs')
    plate_number = models.CharField(max_length=20)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plate_number} detected at {self.slot} by {self.camera}"
