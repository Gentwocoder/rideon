from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, permission_classes
from .serializers import (CustomTokenSerializer, UserSerializer, RegisterSerializer, 
                        DriverProfileSerializer, LoginSerializer, PhoneVerificationSerializer,
                        SendVerificationCodeSerializer, VerifyPhoneCodeSerializer)
from .models import CustomUser, DriverProfile, PhoneVerification
from .sms_service import sms_service

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            # Handle validation errors with detailed messages
            error_details = {}
            for field, errors in serializer.errors.items():
                if isinstance(errors, list):
                    error_details[field] = errors[0] if errors else "Invalid value"
                else:
                    error_details[field] = str(errors)
            
            return Response({
                'message': 'Registration failed. Please check the errors below.',
                'errors': error_details,
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = serializer.save()
            
            return Response({
                'message': 'Registration successful! Please check your email to verify your account.',
                'user': {
                    'email': user.email,
                    'user_type': user.user_type,
                    'phone_number': user.phone_number,
                    'is_email_verified': user.is_email_verified,
                    'is_phone_verified': user.is_phone_verified
                },
                'status': 'success'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Registration error:", str(e))  # Debug logging
            
            # Handle database integrity errors
            error_message = str(e).lower()
            if 'unique constraint' in error_message or 'already exists' in error_message:
                if 'email' in error_message:
                    return Response({
                        'message': 'Registration failed. Please check the errors below.',
                        'errors': {'email': 'An account with this email already exists'},
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)
                elif 'phone' in error_message:
                    return Response({
                        'message': 'Registration failed. Please check the errors below.',
                        'errors': {'phone_number': 'An account with this phone number already exists'},
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'message': 'Registration failed due to an unexpected error.',
                'errors': {'detail': 'An unexpected error occurred. Please try again.'},
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenSerializer

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        if not serializer:
            return Response({"error": "User not found"}, status=404)
        return Response(serializer.data)

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DriverProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DriverProfileSerializer

    def get(self, request):
        try:
            driver_profile = request.user.profile
            serializer = self.serializer_class(driver_profile)
            return Response(serializer.data)
        except DriverProfile.DoesNotExist:
            return Response({"error": "Driver profile not found"}, status=404)
    
    def put(self, request):
        try:
            driver_profile = request.user.profile
            serializer = self.serializer_class(driver_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except DriverProfile.DoesNotExist:
            return Response({"error": "Driver profile not found"}, status=404)
    
    def delete(self, request):
        try:
            request.user.profile.delete()
            return Response(status=204)
        except DriverProfile.DoesNotExist:
            return Response({"error": "Driver profile not found"}, status=404)
    
    def post(self, request):
        # Create a new driver profile for the authenticated user
        if hasattr(request.user, 'profile'):
            return Response({"error": "Driver profile already exists"}, status=400)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"message": "Invalid credentials", "status": "failed"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_email_verified:
            return Response({"message": "Email is not verified", "status": "failed"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({"message": "Account is not active, contact the admin", "status": "failed"},
                            status=status.HTTP_400_BAD_REQUEST)

        tokens = super().post(request)

        return Response({"message": "Logged in successfully", "tokens": tokens.data,
                         "data": {"email": user.email, "user_type": user.user_type}, "status": "success"},
                        status=status.HTTP_200_OK)
    

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            user = get_object_or_404(CustomUser, email_verification_token=token)
            
            if user.is_email_verified:
                return Response({
                    "message": "Email is already verified",
                    "status": "info"
                }, status=status.HTTP_200_OK)
            
            user.is_email_verified = True
            user.email_verification_token = None  # Clear the token after verification
            user.save()
            
            return Response({
                "message": "Email verified successfully! You can now log in to your account.",
                "status": "success"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "message": "Invalid or expired verification token",
                "status": "error"
            }, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated requests

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            
            if not refresh_token:
                # If no refresh token provided, consider it a successful logout
                return Response({
                    "message": "Logout successful"
                }, status=status.HTTP_200_OK)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message": "Logout successful"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Even if token blacklisting fails, consider logout successful
            # This handles cases where token is already invalid/expired
            print(f"Logout error (non-critical): {str(e)}")  # Debug log
            return Response({
                "message": "Logout successful"
            }, status=status.HTTP_200_OK)


# Phone Verification Views
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_verification_code(request):
    """Send SMS verification code to user's phone number"""
    
    serializer = SendVerificationCodeSerializer(data=request.data)
    
    if not serializer.is_valid():
        print(f"DEBUG: Serializer errors: {serializer.errors}")  # Debug log
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    phone_number = serializer.validated_data['phone_number']
    user = request.user
    
    
    # Check if phone number belongs to the current user
    if user.phone_number != phone_number:
        print(f"DEBUG: Phone mismatch - User: {user.phone_number}, Requested: {phone_number}")  # Debug log
        return Response({
            'error': 'Phone number does not match your account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if phone is already verified
    if user.is_phone_verified:
        return Response({
            'error': 'Phone number is already verified'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    # Check for recent verification attempts (rate limiting)
    recent_attempts = PhoneVerification.objects.filter(
        user=user,
        phone_number=phone_number,
        created_at__gte=timezone.now() - timezone.timedelta(minutes=1)
    ).count()
        
    if recent_attempts >= 3:
        return Response({
            'error': 'Too many verification attempts. Please wait before requesting another code.'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
    # Create new verification record
    verification = PhoneVerification.objects.create(
        user=user,
        phone_number=phone_number
    )
    
    # Send SMS using the configured SMS service
    message = f"Your RideOn verification code is: {verification.verification_code}. This code expires in 10 minutes."
    sms_success = sms_service._send_via_twilio(phone_number, message)
    
    if sms_success:
        return Response({
            'message': 'Verification code sent successfully',
            'expires_at': verification.expires_at
        }, status=status.HTTP_200_OK)
    else:
        # Delete the verification record if SMS failed
        verification.delete()
        return Response({
            'error': 'Failed to send verification code. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_phone_code(request):
    """Verify the SMS code sent to user's phone number"""
    serializer = VerifyPhoneCodeSerializer(data=request.data)
    
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        verification_code = serializer.validated_data['verification_code']
        user = request.user
        
        # Check if phone number belongs to the current user
        if user.phone_number != phone_number:
            return Response({
                'error': 'Phone number does not match your account'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if phone is already verified
        if user.is_phone_verified:
            return Response({
                'error': 'Phone number is already verified'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Find the most recent verification record
        verification = PhoneVerification.objects.filter(
            user=user,
            phone_number=phone_number,
            is_verified=False
        ).order_by('-created_at').first()
        
        if not verification:
            return Response({
                'error': 'No verification request found. Please request a new verification code.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if verification is still valid
        if not verification.is_valid():
            return Response({
                'error': 'Verification code has expired or exceeded maximum attempts. Please request a new code.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Increment attempts
        verification.attempts += 1
        verification.save()
        
        # Check if code matches
        if verification.verification_code != verification_code:
            remaining_attempts = 3 - verification.attempts
            if remaining_attempts > 0:
                return Response({
                    'error': f'Invalid verification code. You have {remaining_attempts} attempts remaining.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'Invalid verification code. Maximum attempts exceeded. Please request a new code.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verification successful
        verification.is_verified = True
        verification.save()
        
        # Update user's phone verification status
        user.is_phone_verified = True
        user.save()
        
        # Send welcome message
        welcome_message = f"Welcome to RideOn! Your phone number has been verified successfully. You're all set to {'start driving' if user.user_type == 'driver' else 'book rides'}!"
        sms_service._send_via_twilio(phone_number, welcome_message)
        
        return Response({
            'message': 'Phone number verified successfully!',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def phone_verification_status(request):
    """Get phone verification status for the current user"""
    user = request.user
    
    # Get recent verification attempts
    recent_verifications = PhoneVerification.objects.filter(
        user=user,
        phone_number=user.phone_number
    ).order_by('-created_at')[:5]
    
    return Response({
        'is_phone_verified': user.is_phone_verified,
        'phone_number': user.phone_number,
        'recent_verifications': PhoneVerificationSerializer(recent_verifications, many=True).data
    }, status=status.HTTP_200_OK)