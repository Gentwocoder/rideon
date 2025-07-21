from rest_framework import serializers
from django.utils import timezone
from .models import Ride, RideRequest, RideMessage, Rating
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


class RatingSerializer(serializers.ModelSerializer):
    rater = UserSerializer(read_only=True)
    rated_user = UserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['rater', 'rated_user', 'created_at', 'updated_at']


class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rating', 'comment', 'punctuality', 'communication', 'cleanliness', 'professionalism']
    
    def validate_rating(self, value):
        """Validate that rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
    def validate_punctuality(self, value):
        """Validate punctuality rating"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Punctuality rating must be between 1 and 5")
        return value
    
    def validate_communication(self, value):
        """Validate communication rating"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Communication rating must be between 1 and 5")
        return value
    
    def validate_cleanliness(self, value):
        """Validate cleanliness rating"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Cleanliness rating must be between 1 and 5")
        return value
    
    def validate_professionalism(self, value):
        """Validate professionalism rating"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Professionalism rating must be between 1 and 5")
        return value