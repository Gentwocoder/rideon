from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ride(models.Model):
    RIDE_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_driver', null=True, blank=True)
    
    pickup_location = models.CharField(max_length=255)
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    dropoff_location = models.CharField(max_length=255)
    dropoff_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    status = models.CharField(max_length=15, choices=RIDE_STATUS, default='pending')
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # in minutes
    
    # Scheduling
    scheduled_pickup_time = models.DateTimeField(null=True, blank=True, help_text="When the rider wants to be picked up")
    is_scheduled = models.BooleanField(default=False, help_text="True if this is a scheduled ride, False for immediate")
    
    # Payment
    payment_method = models.CharField(max_length=20, default='cash', choices=[
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
    ])
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Ride {self.id} - {self.rider.email} ({self.status})"

class RideRequest(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['ride', 'driver']
    
    def __str__(self):
        return f"Request for Ride {self.ride.id} by {self.driver.email}"


class RideMessage(models.Model):
    MESSAGE_TYPES = [
        ('driver_arrival', 'Driver Arrival Notification'),
        ('general', 'General Message'),
        ('pickup_delay', 'Pickup Delay'),
        ('route_change', 'Route Change'),
    ]
    
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='general')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message for Ride {self.ride.id} from {self.sender.email}"


class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='ratings')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, help_text="Optional comment about the rating")
    
    # Rating categories
    punctuality = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True, help_text="How punctual was the person")
    communication = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True, help_text="How good was the communication")
    cleanliness = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True, help_text="How clean was the vehicle/person")
    professionalism = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True, help_text="How professional was the person")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['ride', 'rater', 'rated_user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Rating {self.rating}/5 for {self.rated_user.email} by {self.rater.email} (Ride {self.ride.id})"