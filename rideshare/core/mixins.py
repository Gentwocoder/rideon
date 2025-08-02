import jwt
from django.contrib.auth.mixins import AccessMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

class JWTAuthenticationMixin(AccessMixin):
    """
    Mixin that provides JWT authentication for Django template views.
    Checks for valid JWT tokens in cookies or Authorization header.
    """
    
    # URLs that don't require authentication
    login_url = '/login/'
    redirect_field_name = 'next'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Check if user is authenticated via JWT token before dispatching the view.
        """
        if not self.is_jwt_authenticated(request):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def is_jwt_authenticated(self, request):
        """
        Check if the request contains a valid JWT token.
        Looks for token in cookies first, then Authorization header.
        """
        # Get token from various sources
        token = self.get_jwt_token(request)
        
        if not token:
            return False
        
        try:
            # Validate the token using Simple JWT
            UntypedToken(token)
            
            # Decode the token to get user information
            decoded_token = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256']
            )
            
            # Get user from token
            user_id = decoded_token.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    # Attach user to request for use in views
                    request.user = user
                    request.jwt_token = token
                    return True
                except User.DoesNotExist:
                    return False
            
            return False
            
        except (InvalidToken, TokenError, jwt.DecodeError, jwt.ExpiredSignatureError):
            return False
        except Exception as e:
            # Log the exception in production
            print(f"JWT Authentication error: {e}")
            return False
    
    def get_jwt_token(self, request):
        """
        Extract JWT token from request.
        Checks multiple sources: cookies, Authorization header, and query params.
        """
        # Check cookies first (most common for web apps)
        token = request.COOKIES.get('access_token')
        if token:
            return token
        
        # Check Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        
        # Check query parameters (for special cases)
        token = request.GET.get('token')
        if token:
            return token
        
        # Check if token is in session (fallback)
        token = request.session.get('access_token')
        if token:
            return token
        
        return None
    
    def handle_no_permission(self):
        """
        Handle cases where user is not authenticated.
        """
        # If it's an AJAX request, return JSON response
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Authentication required',
                'message': 'Please login to access this page',
                'redirect_url': self.get_login_url()
            }, status=401)
        
        # For regular requests, redirect to login page
        return redirect(f"{self.get_login_url()}?{self.redirect_field_name}={self.request.get_full_path()}")
    
    def get_login_url(self):
        """
        Return the login URL.
        """
        return self.login_url or reverse('login')


class JWTRequiredMixin(JWTAuthenticationMixin):
    """
    Simplified mixin that just requires JWT authentication.
    Use this for views that need authentication but don't need additional logic.
    """
    pass


class RiderRequiredMixin(JWTAuthenticationMixin):
    """
    Mixin that requires the user to be authenticated and be a rider.
    """
    
    def dispatch(self, request, *args, **kwargs):
        if not self.is_jwt_authenticated(request):
            return self.handle_no_permission()
        
        # Check if user has rider permissions
        if not self.is_rider(request.user):
            return self.handle_rider_required()
        
        return super(JWTAuthenticationMixin, self).dispatch(request, *args, **kwargs)
    
    def is_rider(self, user):
        """
        Check if user is a rider. Based on the CustomUser model.
        """
        return hasattr(user, 'user_type') and user.user_type in ['RIDER']
    
    def handle_rider_required(self):
        """
        Handle cases where user is not a rider.
        """
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Rider access required',
                'message': 'This page is only accessible to riders',
            }, status=403)
        
        # Redirect to appropriate page based on user type
        if hasattr(self.request.user, 'user_type') and self.request.user.user_type == 'DRIVER':
            return redirect('driver_dashboard')
        else:
            return redirect('home')


class DriverRequiredMixin(JWTAuthenticationMixin):
    """
    Mixin that requires the user to be authenticated and be a driver.
    """
    
    def dispatch(self, request, *args, **kwargs):
        if not self.is_jwt_authenticated(request):
            return self.handle_no_permission()
        
        # Check if user has driver permissions
        if not self.is_driver(request.user):
            return self.handle_driver_required()
        
        return super(JWTAuthenticationMixin, self).dispatch(request, *args, **kwargs)
    
    def is_driver(self, user):
        """
        Check if user is a driver. Based on the CustomUser model.
        """
        return hasattr(user, 'user_type') and user.user_type in ['DRIVER']
    
    def handle_driver_required(self):
        """
        Handle cases where user is not a driver.
        """
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Driver access required',
                'message': 'This page is only accessible to drivers',
            }, status=403)
        
        # Redirect to appropriate page based on user type
        if hasattr(self.request.user, 'user_type') and self.request.user.user_type == 'RIDER':
            return redirect('dashboard')
        else:
            return redirect('home')


class CSRFExemptMixin:
    """
    Mixin to exempt views from CSRF protection.
    Use with caution and only when necessary.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)