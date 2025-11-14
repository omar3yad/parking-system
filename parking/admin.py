from django.contrib import admin
from .models import ParkingSlot, ParkingTransaction

admin.site.register(ParkingSlot)
admin.site.register(ParkingTransaction)
