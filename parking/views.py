from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ParkingSlot, ParkingTransaction
from .serializers import ParkingSlotSerializer, ParkingTransactionSerializer, EnterCarSerializer ,ExitCarSerializer
from users.models import Car
from django.utils import timezone

class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

class ParkingTransactionViewSet(viewsets.ModelViewSet):
    queryset = ParkingTransaction.objects.all()
    serializer_class = ParkingTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

# entry action
    @action(detail=False, methods=['put'], url_path='enter', serializer_class=EnterCarSerializer)
    def enter_car(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.validated_data['car']
        slot = serializer.validated_data['slot']

        # تحقق من أن الموقف متاح
        if slot.status != 'available':
            return Response({'error': 'Parking slot is not available.'}, status=status.HTTP_400_BAD_REQUEST)

        # إنشاء معاملة جديدة
        transaction = ParkingTransaction.objects.create(
            car=car,
            slot=slot,
            entry_time=timezone.now(),
            status='active'
        )

        # تحديث حالة الموقف
        slot.status = 'occupied'
        slot.save()

        return Response(EnterCarSerializer(transaction).data, status=status.HTTP_201_CREATED)

    # exit action
    @action(detail=False, methods=['put'], url_path='exit-car', serializer_class=ExitCarSerializer)
    def exit_car(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_id = serializer.validated_data['id']

        # اجلب الترانزكشن
        try:
            transaction = ParkingTransaction.objects.get(id=transaction_id, status='active')
        except ParkingTransaction.DoesNotExist:
            return Response({'error': 'Active transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

        # سجل وقت الخروج
        exit_time = timezone.now()
        transaction.exit_time = exit_time

        # حساب الوقت بالساعة
        duration = (exit_time - transaction.entry_time).total_seconds() / 3600
        duration_hours = max(1, round(duration))   # الحد الأدنى ساعة واحدة

        # حساب الفلوس
        hourly_rate = 10  # مثال: 10 جنيه للساعة
        fee = duration_hours * hourly_rate
        transaction.fee = fee

        # تغيير الحالة
        transaction.status = 'completed'
        transaction.save()

        # تفريغ مكان الركنة
        slot = transaction.slot
        slot.status = "available"
        slot.save()

        return Response({
            "message": "Car exited successfully.",
            "id": transaction.id,
            "entry_time": transaction.entry_time,
            "exit_time": transaction.exit_time,
            "hours": duration_hours,
            "fee": fee,
            "slot": slot.slot_number,
        }, status=status.HTTP_200_OK)

# exit action
    @action(detail=False, methods=['Post'], url_path='exit', serializer_class=ExitCarSerializer)
    def exit_car_old(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_id = serializer.validated_data['id']

        # اجلب الترانزكشن
        try:
            transaction = ParkingTransaction.objects.get(id=transaction_id, status='active')
        except ParkingTransaction.DoesNotExist:
            return Response({'error': 'Active transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

        # سجل وقت الخروج
        exit_time = timezone.now()
        transaction.exit_time = exit_time

        # حساب الوقت بالساعة
        duration = (exit_time - transaction.entry_time).total_seconds() / 3600
        duration_hours = max(1, round(duration))   # الحد الأدنى ساعة واحدة

        # حساب الفلوس
        hourly_rate = 10  # مثال: 10 جنيه للساعة
        fee = duration_hours * hourly_rate
        transaction.fee = fee

        # تغيير الحالة
        transaction.status = 'completed'
        transaction.save()

        # تفريغ مكان الركنة
        slot = transaction.slot
        slot.status = "available"
        slot.save()

        return Response({
            "message": "Car exited successfully.",
            "id": transaction.id,
            "entry_time": transaction.entry_time,
            "exit_time": transaction.exit_time,
            "hours": duration_hours,
            "fee": fee,
            "slot": slot.slot_number,
        }, status=status.HTTP_200_OK)
