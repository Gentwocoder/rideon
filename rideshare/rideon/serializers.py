from rest_framework import serializers
from .models import Ride, RideRequest
from core.serializers import UserSerializer

class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)
    
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ['rider', 'created_at', 'updated_at']

class RideCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['pickup_location', 'pickup_latitude', 'pickup_longitude', 
                 'dropoff_location', 'dropoff_latitude', 'dropoff_longitude', 'notes']

class RideRequestSerializer(serializers.ModelSerializer):
    driver = UserSerializer(read_only=True)
    
    class Meta:
        model = RideRequest
        fields = '__all__'
        read_only_fields = ['driver', 'created_at']