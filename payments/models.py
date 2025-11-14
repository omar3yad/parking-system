from django.db import models
from parking.models import ParkingTransaction

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    )

    transaction = models.ForeignKey(ParkingTransaction, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction} - {self.amount} via {self.payment_method}"
