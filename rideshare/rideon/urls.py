from django.urls import path
from . import views

urlpatterns = [
    path('', views.rides, name='rides'),
    path('fare-info/', views.fare_info, name='fare_info'),
    path('available/', views.available_rides, name='available_rides'),
    path('<int:ride_id>/accept/', views.accept_ride, name='accept_ride'),
    path('<int:ride_id>/status/', views.update_ride_status, name='update_ride_status'),
    path('<int:ride_id>/messages/', views.ride_messages, name='ride_messages'),
    path('<int:ride_id>/arrival/', views.driver_arrival_notification, name='driver_arrival'),
    
    # Rating endpoints
    path('<int:ride_id>/ratings/', views.ride_ratings, name='ride_ratings'),
    path('ratings/<int:rating_id>/', views.rating_detail, name='rating_detail'),
    path('users/<int:user_id>/ratings/', views.user_ratings, name='user_ratings'),
    path('my-ratings/', views.user_ratings, name='my_ratings'),
]