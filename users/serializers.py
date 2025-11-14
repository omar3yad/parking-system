from rest_framework import serializers
from .models import User, Car

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class CarSerializer(serializers.ModelSerializer):
    # owner = UserSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'plate_number', 'car_type', 'owner', 'created_at']
