from django.db import models
from django.utils import timezone
from users.models import Car  # الربط مع app users
import math

# ----------------------------
# المواقف (Slots)
# ----------------------------
class ParkingSlot(models.Model):
    SLOT_TYPE_CHOICES = (
        ('compact', 'Compact'),
        ('regular', 'Regular'),
        ('large', 'Large'),
    )
    SLOT_STATUS_CHOICES = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
    )
    slot_number = models.CharField(max_length=10, unique=True)
    slot_type = models.CharField(max_length=10, choices=SLOT_TYPE_CHOICES, default='regular')
    status = models.CharField(max_length=10, choices=SLOT_STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Slot {self.slot_number} ({self.status})"

# ----------------------------
# حركة السيارات (Transactions)
# ----------------------------
class ParkingTransaction(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
    )

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='transactions')
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE, related_name='transactions')
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        # حساب الرسوم تلقائيًا داخل المودل
        if self.exit_time:
            duration_hours = (self.exit_time - self.entry_time).total_seconds() / 3600
            self.fee = math.ceil(duration_hours) * 10
        # حساب الرسوم تلقائيًا داخل المودل
        if self.entry_time and self.exit_time:
            duration_hours = (self.exit_time - self.entry_time).total_seconds() / 3600
            self.fee = math.ceil(duration_hours) * 10

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.car} in {self.slot} ({self.status})"
