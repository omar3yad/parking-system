from django.urls import path
from .views import DashboardView
from .views import indexx

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('index', indexx, name='index'),
]
