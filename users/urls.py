from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CarViewSet
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('frontcars/', views.cars_view, name='frontcars'),
]
