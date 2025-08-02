from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse

class Command(BaseCommand):
    help = 'Test authentication redirect loop fix'
    
    def handle(self, *args, **options):
        self.stdout.write("🔄 Testing Login Redirect Loop Fix")
        self.stdout.write("=" * 50)
        
        client = Client()
        
        # Test 1: Access login page without authentication
        self.stdout.write("\n1. Testing unauthenticated access to login page:")
        try:
            response = client.get('/login/')
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("   ✅ Login page accessible without authentication"))
                self.stdout.write(f"   Status: {response.status_code}")
            else:
                self.stdout.write(self.style.ERROR(f"   ❌ Login page returned status: {response.status_code}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Error accessing login page: {e}"))
        
        # Test 2: Access protected pages without authentication
        self.stdout.write("\n2. Testing unauthenticated access to protected pages:")
        protected_urls = [
            '/dashboard/',
            '/driver-dashboard/',
            '/request-ride/',
            '/my-profile/',
        ]
        
        for url in protected_urls:
            try:
                response = client.get(url)
                if response.status_code == 302:  # Redirect to login
                    self.stdout.write(self.style.SUCCESS(f"   ✅ {url} correctly redirects to login"))
                else:
                    self.stdout.write(self.style.WARNING(f"   ⚠️  {url} returned status: {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ Error accessing {url}: {e}"))
        
        # Test 3: Access public pages
        self.stdout.write("\n3. Testing access to public pages:")
        public_urls = [
            '/',
            '/register/',
            '/forgot-password/',
        ]
        
        for url in public_urls:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f"   ✅ {url} accessible"))
                else:
                    self.stdout.write(self.style.WARNING(f"   ⚠️  {url} returned status: {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ Error accessing {url}: {e}"))
        
        # Test 4: Check JWT token validation
        self.stdout.write("\n4. Testing JWT authentication system:")
        
        try:
            from core.mixins import JWTAuthenticationMixin
            from django.test import RequestFactory
            
            mixin = JWTAuthenticationMixin()
            factory = RequestFactory()
            
            # Test without token
            request = factory.get('/dashboard/')
            from django.contrib.sessions.backends.db import SessionStore
            request.session = SessionStore()
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()
            
            if not mixin.is_jwt_authenticated(request):
                self.stdout.write(self.style.SUCCESS("   ✅ JWT mixin correctly rejects requests without token"))
            else:
                self.stdout.write(self.style.ERROR("   ❌ JWT mixin should reject requests without token"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Error testing JWT mixin: {e}"))
        
        self.stdout.write("\n🎉 Authentication Test Complete!")
        self.stdout.write("\n📋 Summary:")
        self.stdout.write("• Login page should be accessible without authentication")
        self.stdout.write("• Protected pages should redirect to login when not authenticated")
        self.stdout.write("• Public pages should always be accessible")
        self.stdout.write("• No infinite redirect loops should occur")
        
        self.stdout.write("\n💡 To test manually:")
        self.stdout.write("1. Clear browser cookies and localStorage")
        self.stdout.write("2. Visit http://localhost:8000/login/")
        self.stdout.write("3. Should load login page without redirects")
        self.stdout.write("4. Try visiting http://localhost:8000/dashboard/")
        self.stdout.write("5. Should redirect to login page")
