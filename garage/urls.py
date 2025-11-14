from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("frontend.urls")),
    path('api/users/', include('users.urls')),
    path('api/parking/', include('parking.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/camera_ocr/', include('camera_ocr.urls')),
]
