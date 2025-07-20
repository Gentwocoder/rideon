from django.contrib import admin
from .models import Ride, RideRequest, RideMessage

# Register your models here.
admin.site.register(Ride)
admin.site.register(RideRequest)
admin.site.register(RideMessage)
admin.site.site_header = "RideOn Admin"
admin.site.site_title = "RideOn Admin Portal"
admin.site.index_title = "Welcome to the RideOn Admin Portal"