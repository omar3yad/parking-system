from rest_framework import viewsets, permissions
from .models import User, Car
from .serializers import UserSerializer, CarSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Car

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    # مثال endpoint لتسجيل سيارة جديدة للمستخدم
    @action(detail=False, methods=['post'])
    def add_car(self, request):
        user = request.user
        plate_number = request.data.get('plate_number')
        car_type = request.data.get('car_type', '')
        car = Car.objects.create(owner=user, plate_number=plate_number, car_type=car_type)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    # مثال endpoint لجلب جميع السيارات للمستخدم الحال

# Template-based login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'form': {'errors': True}})
    return render(request, 'users/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

@login_required
def cars_view(request):
    if not hasattr(request.user, 'id') or not request.user.is_authenticated:
        return redirect('login')
    cars = Car.objects.filter(owner=request.user)
    return render(request, 'users/cars.html', {'cars': cars})
