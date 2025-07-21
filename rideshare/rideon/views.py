# from django.shortcuts import render
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework import viewsets
# from django.db.models import Q
# from .models import Ride, RideRequest
# from .serializers import RideSerializer, RideCreateSerializer, RideRequestSerializer

# # Create your views here.
# class RideView(viewsets.ViewSet):
#     queryset = Ride.objects.all()
#     permission_classes = [permissions.IsAuthenticated]
    
#     def list(self, request):
#         user_rides = Ride.objects.filter(
#             Q(rider=request.user) | Q(driver=request.user)
#         )
#         serializer = RideSerializer(user_rides, many=True)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = RideCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             ride = serializer.save(rider=request.user)
#             return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class AvailableRidesView(generics.ListAPIView):
#     queryset = Ride.objects.filter(status='pending')
#     serializer_class = RideSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.exclude(rider=self.request.user)
    
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Avg
from .models import Ride, RideRequest, RideMessage, Rating
from .serializers import RideSerializer, RideCreateSerializer, RideRequestSerializer, RideMessageSerializer, RatingSerializer, RatingCreateSerializer
# from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
# @extend_schema(responses={200: RideSerializer(many=True)},
#                parameters=[
#                    OpenApiParameter(name='status', type=str, description='Filter rides by status'),
#                    OpenApiParameter(name='driver', type=str, description='Filter rides by driver ID')
#                ])
def rides(request):
    if request.method == 'GET':
        # Get rides for the current user
        user_rides = Ride.objects.filter(
            Q(rider=request.user) | Q(driver=request.user)
        )
        serializer = RideSerializer(user_rides, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RideCreateSerializer(data=request.data)
        if serializer.is_valid():
            ride = serializer.save(rider=request.user)
            return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @extend_schema(responses={200: RideSerializer(many=True)})
def available_rides(request):
    """Get all pending rides for drivers"""
    pending_rides = Ride.objects.filter(status='pending').exclude(rider=request.user)
    serializer = RideSerializer(pending_rides, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @extend_schema(responses={200: RideSerializer})
def accept_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id, status='pending')
        ride.driver = request.user
        ride.status = 'accepted'
        ride.save()
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @extend_schema(responses={200: RideSerializer})
def update_ride_status(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        
        # Check if user is involved in the ride
        if ride.rider != request.user and ride.driver != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status in ['in_progress', 'completed', 'cancelled']:
            ride.status = new_status
            ride.save()
            return Response(RideSerializer(ride).data)
        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ride_messages(request, ride_id):
    """Get messages for a ride or send a new message"""
    try:
        ride = Ride.objects.get(id=ride_id)
        
        # Check if user is involved in the ride
        if ride.rider != request.user and ride.driver != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'GET':
            messages = RideMessage.objects.filter(ride=ride)
            serializer = RideMessageSerializer(messages, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = RideMessageSerializer(data=request.data)
            if serializer.is_valid():
                message = serializer.save(ride=ride, sender=request.user)
                return Response(RideMessageSerializer(message).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def driver_arrival_notification(request, ride_id):
    """Driver notifies rider of arrival"""
    try:
        ride = Ride.objects.get(id=ride_id, driver=request.user)
        
        # Create arrival notification message
        message = RideMessage.objects.create(
            ride=ride,
            sender=request.user,
            message_type='driver_arrival',
            message=f"I've arrived at the pickup location: {ride.pickup_location}. Please come out when you're ready."
        )
        
        return Response(RideMessageSerializer(message).data, status=status.HTTP_201_CREATED)
    
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ride_ratings(request, ride_id):
    """Get ratings for a ride or create a new rating"""
    try:
        ride = Ride.objects.get(id=ride_id)
        
        # Check if user is involved in the ride
        if ride.rider != request.user and ride.driver != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        # Only allow rating for completed rides
        if ride.status != 'completed':
            return Response({'error': 'Can only rate completed rides'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'GET':
            ratings = Rating.objects.filter(ride=ride)
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            # Determine who is being rated
            if request.user == ride.rider:
                # Rider is rating the driver
                rated_user = ride.driver
            elif request.user == ride.driver:
                # Driver is rating the rider
                rated_user = ride.rider
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            
            if not rated_user:
                return Response({'error': 'No user to rate'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user has already rated
            existing_rating = Rating.objects.filter(
                ride=ride, 
                rater=request.user, 
                rated_user=rated_user
            ).first()
            
            if existing_rating:
                return Response({'error': 'You have already rated this ride'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = RatingCreateSerializer(data=request.data)
            if serializer.is_valid():
                rating = serializer.save(
                    ride=ride,
                    rater=request.user,
                    rated_user=rated_user
                )
                return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_ratings(request, user_id=None):
    """Get ratings for a specific user or current user"""
    target_user_id = user_id or request.user.id
    
    try:
        # Get all ratings received by the user
        ratings = Rating.objects.filter(rated_user_id=target_user_id)
        
        # Calculate average ratings
        avg_overall = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        avg_punctuality = ratings.aggregate(Avg('punctuality'))['punctuality__avg'] or 0
        avg_communication = ratings.aggregate(Avg('communication'))['communication__avg'] or 0
        avg_cleanliness = ratings.aggregate(Avg('cleanliness'))['cleanliness__avg'] or 0
        avg_professionalism = ratings.aggregate(Avg('professionalism'))['professionalism__avg'] or 0
        
        ratings_data = RatingSerializer(ratings, many=True).data
        
        return Response({
            'ratings': ratings_data,
            'total_ratings': ratings.count(),
            'averages': {
                'overall': round(avg_overall, 2),
                'punctuality': round(avg_punctuality, 2),
                'communication': round(avg_communication, 2),
                'cleanliness': round(avg_cleanliness, 2),
                'professionalism': round(avg_professionalism, 2)
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def rating_detail(request, rating_id):
    """Update or delete a specific rating"""
    try:
        rating = Rating.objects.get(id=rating_id, rater=request.user)
        
        if request.method == 'PUT':
            serializer = RatingCreateSerializer(rating, data=request.data, partial=True)
            if serializer.is_valid():
                rating = serializer.save()
                return Response(RatingSerializer(rating).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            rating.delete()
            return Response({'message': 'Rating deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    except Rating.DoesNotExist:
        return Response({'error': 'Rating not found'}, status=status.HTTP_404_NOT_FOUND)