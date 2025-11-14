from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Camera, OCRLog
from .serializers import CameraSerializer, OCRLogSerializer
from parking.models import ParkingSlot
from users.models import Car

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [permissions.IsAuthenticated]

class OCRLogViewSet(viewsets.ModelViewSet):
    queryset = OCRLog.objects.all()
    serializer_class = OCRLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def detect_car(self, request):
        """تسجيل كشف السيارة بواسطة الكاميرا"""
        camera_id = request.data.get('camera_id')
        slot_id = request.data.get('slot_id')
        plate_number = request.data.get('plate_number')

        try:
            camera = Camera.objects.get(id=camera_id)
            slot = ParkingSlot.objects.get(id=slot_id)
        except (Camera.DoesNotExist, ParkingSlot.DoesNotExist):
            return Response({"error": "Camera or Slot not found"}, status=status.HTTP_404_NOT_FOUND)

        # إنشاء سجل OCR
        ocr_log = OCRLog.objects.create(camera=camera, slot=slot, plate_number=plate_number)

        # تحديث حالة الموقف تلقائيًا (إذا عايز)
        try:
            from parking.models import ParkingTransaction
            car, _ = Car.objects.get_or_create(plate_number=plate_number)
            active_transaction = ParkingTransaction.objects.filter(car=car, status='active').last()
            if not active_transaction:
                # إذا مفيش Transaction شغال، نعتبرها دخول جديد
                ParkingTransaction.objects.create(car=car, slot=slot)
            slot.is_occupied = True
            slot.save()
        except Exception as e:
            pass  # لو في مشكلة، نتخطى التحديث التلقائي

        serializer = OCRLogSerializer(ocr_log)
        return Response(serializer.data)
