from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CameraViewSet, OCRLogViewSet

router = DefaultRouter()
router.register(r'cameras', CameraViewSet)
router.register(r'ocr_logs', OCRLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
