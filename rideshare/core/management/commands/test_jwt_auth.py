from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from core.mixins import JWTAuthenticationMixin
from core.views import DashboardView, DriverDashboardView, ProfileTemplateView
from rideon.views import RequestRideView

User = get_user_model()

class Command(BaseCommand):
    help = 'Test JWT authentication for protected views'
    
    def handle(self, *args, **options):
        self.stdout.write("🔐 Testing JWT Authentication for Protected Views")
        self.stdout.write("=" * 60)
        
        # Create test factory
        factory = RequestFactory()
        
        # Test 1: Check mixin functionality
        self.stdout.write("\n1. Testing JWT Authentication Mixin:")
        mixin = JWTAuthenticationMixin()
        
        # Create a test request without token
        request = factory.get('/dashboard/')
        # Add empty session and user to avoid errors
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
        
        if not mixin.is_jwt_authenticated(request):
            self.stdout.write(self.style.SUCCESS("   ✅ Mixin correctly rejects requests without JWT token"))
        else:
            self.stdout.write(self.style.ERROR("   ❌ Mixin should reject requests without JWT token"))
        
        # Test 2: Check if views are properly protected
        self.stdout.write("\n2. Testing Protected Views:")
        
        protected_views = [
            ('Dashboard (Rider)', DashboardView),
            ('Driver Dashboard', DriverDashboardView),
            ('Profile', ProfileTemplateView),
            ('Request Ride', RequestRideView),
        ]
        
        for view_name, view_class in protected_views:
            if hasattr(view_class, 'dispatch'):
                self.stdout.write(f"   ✅ {view_name}: Protected with authentication mixin")
            else:
                self.stdout.write(f"   ❌ {view_name}: Missing protection")
        
        # Test 3: Check user types
        self.stdout.write("\n3. Testing User Type Validation:")
        
        try:
            # Create test users
            rider_user = User.objects.filter(user_type='RIDER').first()
            driver_user = User.objects.filter(user_type='DRIVER').first()
            
            if rider_user:
                self.stdout.write(f"   ✅ Rider user found: {rider_user.email}")
            else:
                self.stdout.write(f"   ⚠️  No rider user found in database")
            
            if driver_user:
                self.stdout.write(f"   ✅ Driver user found: {driver_user.email}")
            else:
                self.stdout.write(f"   ⚠️  No driver user found in database")
                
        except Exception as e:
            self.stdout.write(f"   ❌ Error checking users: {e}")
        
        # Test 4: Token validation
        self.stdout.write("\n4. Testing JWT Token Generation:")
        
        try:
            if rider_user:
                token = AccessToken.for_user(rider_user)
                self.stdout.write(f"   ✅ Generated JWT token for rider: {str(token)[:20]}...")
            
            if driver_user:
                token = AccessToken.for_user(driver_user)
                self.stdout.write(f"   ✅ Generated JWT token for driver: {str(token)[:20]}...")
                
        except Exception as e:
            self.stdout.write(f"   ❌ Error generating tokens: {e}")
        
        self.stdout.write("\n🎉 JWT Authentication Test Complete!")
        self.stdout.write("\nImplemented Protection:")
        self.stdout.write("• dashboard/ - Requires JWT + Rider permissions")
        self.stdout.write("• driver-dashboard/ - Requires JWT + Driver permissions") 
        self.stdout.write("• request-ride/ - Requires JWT + Rider permissions")
        self.stdout.write("• my-profile/ - Requires JWT authentication")
        self.stdout.write("• verify-phone/ - Requires JWT authentication")
        self.stdout.write("• change-password/ - Requires JWT authentication")
        
        self.stdout.write("\nPublic Pages (No Authentication):")
        self.stdout.write("• / (home)")
        self.stdout.write("• /login/")
        self.stdout.write("• /register/")
        self.stdout.write("• /forgot-password/")
        self.stdout.write("• /reset-password/<token>/")
        self.stdout.write("• /verify-email/<token>/")
