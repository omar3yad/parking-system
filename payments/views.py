from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from parking.models import ParkingTransaction

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def pay_transaction(self, request):
        """تسجيل دفع لمعاملة محددة"""
        transaction_id = request.data.get('transaction_id')
        payment_method = request.data.get('payment_method', 'cash')

        try:
            transaction = ParkingTransaction.objects.get(id=transaction_id)
        except ParkingTransaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        if transaction.status != 'completed':
            return Response({"error": "Transaction not completed yet"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            transaction=transaction,
            amount=transaction.fee,
            payment_method=payment_method
        )
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
