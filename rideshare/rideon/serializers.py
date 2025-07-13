from rest_framework import serializers
from django.utils import timezone
from .models import Ride, RideRequest, RideMessage
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
                 'dropoff_location', 'dropoff_latitude', 'dropoff_longitude', 
                 'scheduled_pickup_time', 'is_scheduled', 'payment_method', 'notes']
    
    def validate_scheduled_pickup_time(self, value):
        """Validate that scheduled pickup time is in the future"""
        if value and value <= timezone.now():
            raise serializers.ValidationError("Scheduled pickup time must be in the future")
        return value

class RideRequestSerializer(serializers.ModelSerializer):
    driver = UserSerializer(read_only=True)
    
    class Meta:
        model = RideRequest
        fields = '__all__'
        read_only_fields = ['driver', 'created_at']


class RideMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = RideMessage
        fields = '__all__'
        read_only_fields = ['id', 'ride', 'sender', 'created_at']