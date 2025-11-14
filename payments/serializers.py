from rest_framework import serializers
from .models import Payment
from parking.serializers import ParkingTransactionSerializer

class PaymentSerializer(serializers.ModelSerializer):
    # transaction = ParkingTransactionSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'transaction', 'amount', 'payment_method', 'paid_at']

