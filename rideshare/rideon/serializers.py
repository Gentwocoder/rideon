from rest_framework import serializers
from django.utils import timezone
import math
from .models import Ride, RideRequest, RideMessage, Rating
from .utils import calculate_fare
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
    
    def validate_pickup_location(self, value):
        """Validate that pickup location is a proper address, not coordinates"""
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError("Please provide a valid pickup address")
        
        # Check if it looks like coordinates (contains only numbers, commas, periods, and spaces)
        import re
        coordinate_pattern = r'^[-+]?[0-9]*\.?[0-9]+\s*,\s*[-+]?[0-9]*\.?[0-9]+$'
        if re.match(coordinate_pattern, value.strip()):
            raise serializers.ValidationError(
                "Please enter a street address (e.g., 'Victoria Island, Lagos') instead of coordinates"
            )
        
        return value
    
    def validate_dropoff_location(self, value):
        """Validate that dropoff location is a proper address, not coordinates"""
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError("Please provide a valid dropoff address")
        
        # Check if it looks like coordinates
        import re
        coordinate_pattern = r'^[-+]?[0-9]*\.?[0-9]+\s*,\s*[-+]?[0-9]*\.?[0-9]+$'
        if re.match(coordinate_pattern, value.strip()):
            raise serializers.ValidationError(
                "Please enter a street address (e.g., 'Ikeja, Lagos') instead of coordinates"
            )
        
        return value
    
    def create(self, validated_data):
        """Create ride with calculated distance and fare"""
        ride = super().create(validated_data)
        
        # Calculate distance using Haversine formula
        if (ride.pickup_latitude and ride.pickup_longitude and 
            ride.dropoff_latitude and ride.dropoff_longitude):
            distance = self.calculate_distance(
                float(ride.pickup_latitude), float(ride.pickup_longitude),
                float(ride.dropoff_latitude), float(ride.dropoff_longitude)
            )
            ride.distance = round(distance, 2)
            
            # Calculate fare using centralized function
            ride.fare = calculate_fare(distance)
            
            ride.save()
        
        return ride
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Radius of the Earth in kilometers
        
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Calculate differences
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Haversine formula
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance

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