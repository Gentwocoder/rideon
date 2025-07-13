from django.urls import path
from . import views

urlpatterns = [
    path('', views.rides, name='rides'),
    path('available/', views.available_rides, name='available_rides'),
    path('<int:ride_id>/accept/', views.accept_ride, name='accept_ride'),
    path('<int:ride_id>/status/', views.update_ride_status, name='update_ride_status'),
    path('<int:ride_id>/messages/', views.ride_messages, name='ride_messages'),
    path('<int:ride_id>/arrival/', views.driver_arrival_notification, name='driver_arrival'),
]