from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkingSlotViewSet, ParkingTransactionViewSet

router = DefaultRouter()
router.register(r'slots', ParkingSlotViewSet)
router.register(r'transactions', ParkingTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
