from django.core.management.base import BaseCommand
from django.conf import settings
from rideon.views import RequestRideView

class Command(BaseCommand):
    help = 'Test Google Maps API key integration'
    
    def handle(self, *args, **options):
        self.stdout.write("🔑 Testing Google Maps API Key Integration")
        self.stdout.write("=" * 50)
        
        # Test 1: Check settings
        api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
        if api_key:
            self.stdout.write(self.style.SUCCESS(f"✅ API Key loaded: {api_key[:10]}..."))
        else:
            self.stdout.write(self.style.ERROR("❌ API Key not found in settings"))
            return
        
        # Test 2: Check view context
        try:
            view = RequestRideView()
            context = view.get_context_data()
            view_api_key = context.get('google_maps_api_key')
            
            if view_api_key == api_key:
                self.stdout.write(self.style.SUCCESS("✅ View context contains correct API key"))
            else:
                self.stdout.write(self.style.ERROR("❌ View context API key mismatch"))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error testing view: {e}"))
            return
        
        self.stdout.write(self.style.SUCCESS("\n🎉 All tests passed! Integration is working correctly."))
        self.stdout.write("\nNext steps:")
        self.stdout.write("1. Visit http://localhost:8000/request-ride/ to test the page")
        self.stdout.write("2. Check browser console for any Google Maps API errors")
        self.stdout.write("3. Verify that the API key is not hardcoded in the HTML source")
