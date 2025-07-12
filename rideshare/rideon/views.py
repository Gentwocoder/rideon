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
from django.db.models import Q
from .models import Ride, RideRequest
from .serializers import RideSerializer, RideCreateSerializer, RideRequestSerializer
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@extend_schema(responses={200: RideSerializer(many=True)},
               parameters=[
                   OpenApiParameter(name='status', type=str, description='Filter rides by status'),
                   OpenApiParameter(name='driver', type=str, description='Filter rides by driver ID')
               ])
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
@extend_schema(responses={200: RideSerializer(many=True)})
def available_rides(request):
    """Get all pending rides for drivers"""
    pending_rides = Ride.objects.filter(status='pending').exclude(rider=request.user)
    serializer = RideSerializer(pending_rides, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@extend_schema(responses={200: RideSerializer})
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
@extend_schema(responses={200: RideSerializer})
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