from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from parking.models import ParkingSlot, ParkingTransaction
from payments.models import Payment
from camera_ocr.models import OCRLog

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # عدد المواقف حسب الحالة
        total_slots = ParkingSlot.objects.count()
        occupied_slots = ParkingSlot.objects.filter(status='occupied').count()
        reserved_slots = ParkingSlot.objects.filter(status='reserved').count()
        available_slots = ParkingSlot.objects.filter(status='available').count()

        # السيارات داخل الجراج الآن
        active_transactions = ParkingTransaction.objects.filter(status='active').count()

        # إجمالي المدفوعات
        total_payments = Payment.objects.all().count()
        total_income = sum([p.amount for p in Payment.objects.all()])

        # آخر 5 سجلات كاميرا
        last_ocr_logs = OCRLog.objects.all().order_by('-detected_at')[:5]
        ocr_data = [
            {
                "plate_number": log.plate_number,
                "slot": log.slot.slot_number,
                "camera": log.camera.camera_name,
                "time": log.detected_at
            } for log in last_ocr_logs
        ]

        data = {
            "total_slots": total_slots,
            "occupied_slots": occupied_slots,
            "reserved_slots": reserved_slots,
            "available_slots": available_slots,
            "active_transactions": active_transactions,
            "total_payments": total_payments,
            "total_income": total_income,
            "last_ocr_logs": ocr_data
        }

        return Response(data)


# dashboard/views.py
from django.shortcuts import render

def indexx(request):
    return render(request, 'index.html')