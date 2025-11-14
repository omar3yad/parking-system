from rest_framework import serializers
from .models import ParkingSlot, ParkingTransaction
from users.serializers import CarSerializer
from users.models import Car


class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = ['id', 'slot_number', 'slot_type', 'status', 'created_at']

class ParkingTransactionSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    slot = ParkingSlotSerializer(read_only=True)

    class Meta:
        model = ParkingTransaction
        fields = ['id', 'car', 'slot', 'entry_time', 'exit_time', 'fee', 'status']

class EnterCarSerializer(serializers.Serializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    slot = serializers.PrimaryKeyRelatedField(queryset=ParkingSlot.objects.all())
    entry_time = serializers.DateTimeField(read_only=True)
    exit_time = serializers.DateTimeField(read_only=True)
    fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)
    
class ExitCarSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
