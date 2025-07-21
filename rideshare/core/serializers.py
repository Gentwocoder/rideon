from rest_framework import serializers
from .models import CustomUser, DriverProfile, PhoneVerification
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.urls import reverse


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_type', 'phone_number', 'is_email_verified', 'is_phone_verified', 'is_active', 'is_staff']
        read_only_fields = ['id', 'email', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    
    # Driver-specific fields (optional)
    license_number = serializers.CharField(required=False, allow_blank=True)
    vehicle_make = serializers.CharField(required=False, allow_blank=True)
    vehicle_model = serializers.CharField(required=False, allow_blank=True)
    vehicle_year = serializers.IntegerField(required=False, allow_null=True)
    vehicle_color = serializers.CharField(required=False, allow_blank=True)
    vehicle_plate = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'user_type', 'password', 'confirm_password',
                 'license_number', 'vehicle_make', 'vehicle_model', 'vehicle_year', 
                 'vehicle_color', 'vehicle_plate']

    def validate_phone_number(self, value):
        """Validate phone number format during registration"""
        if not value:
            raise serializers.ValidationError("Phone number is required")
        
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with country code (e.g., +234)")
        
        # Remove + and check if remaining characters are digits
        digits_only = value[1:]
        if not digits_only.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits after country code")
        
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise serializers.ValidationError("Phone number must be between 10 and 15 digits")
        
        # Check if phone number already exists
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("An account with this phone number already exists")
        
        return value

    def validate_email(self, value):
        """Validate email during registration"""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        
        # If user_type is DRIVER, validate that driver fields are provided
        if attrs.get('user_type') == 'DRIVER':
            driver_fields = ['license_number', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_color', 'vehicle_plate']
            missing_fields = []
            
            for field in driver_fields:
                if not attrs.get(field):
                    missing_fields.append(field)
            
            if missing_fields:
                raise serializers.ValidationError(f"Driver registration requires: {', '.join(missing_fields)}")
        
        return attrs

    def create(self, validated_data):
        # Extract driver-specific data
        driver_data = {}
        driver_fields = ['license_number', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_color', 'vehicle_plate']
        
        for field in driver_fields:
            if field in validated_data:
                driver_data[field] = validated_data.pop(field)
        
        # Remove confirm_password from validated_data
        validated_data.pop('confirm_password', None)
        
        # Create user
        user = CustomUser.objects.create_user(**validated_data)
        
        # Create driver profile if user is a driver
        if user.user_type == 'DRIVER' and driver_data:
            from .models import DriverProfile
            DriverProfile.objects.create(user=user, **driver_data)
        
        # Send verification email
        self.send_verification_email(user)
        
        return user
    
    def send_verification_email(self, user):
        from django.core.mail import send_mail
        from django.urls import reverse
        from django.conf import settings
        
        # Create verification URL - Send users to the frontend verification page
        verification_url = f"http://127.0.0.1:8000/verify-email/{user.email_verification_token}/"
        
        # Email content
        subject = "Welcome to Rideon - Please Verify Your Email"
        message = f"""
Hello!

Welcome to Rideon! We're excited to have you join our ride-sharing community.

To complete your registration and start using Rideon, please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours for security purposes.

If you didn't create an account with Rideon, please ignore this email.

Best regards,
The Rideon Team
        """
        
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #0d6efd;">🚗 Welcome to Rideon!</h1>
                </div>
                
                <p>Hello!</p>
                
                <p>Welcome to Rideon! We're excited to have you join our ride-sharing community.</p>
                
                <p>To complete your registration and start using Rideon, please verify your email address by clicking the button below:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" style="background-color: #0d6efd; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                        Verify Email Address
                    </a>
                </div>
                
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background-color: #f8f9fa; padding: 10px; border-radius: 3px;">
                    {verification_url}
                </p>
                
                <p style="color: #666; font-size: 14px;">
                    <strong>Note:</strong> This link will expire in 24 hours for security purposes.
                </p>
                
                <p style="color: #666; font-size: 14px;">
                    If you didn't create an account with Rideon, please ignore this email.
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="text-align: center; color: #666; font-size: 14px;">
                    Best regards,<br>
                    The Rideon Team
                </p>
            </div>
        </body>
        </html>
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            # You could log this error or handle it differently in production
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150, min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError({"message": "Invalid email format", "status": "failed"})

        return attrs

        
class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = '__all__'
        read_only_fields = ['user', 'rating']

class CustomTokenSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        login_field = attrs.get('email') or attrs.get('phone_number')
        password = attrs.get('password')
        user = authenticate(email=login_field, password=password) or authenticate(phone_number=login_field, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or phone number")
        if not user.is_active:
            raise serializers.ValidationError("User is not active")
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'phone_number': user.phone_number,
            }
        }
    
    def validate(self, attrs):
        user = authenticate(email=attrs.get('email'), password=attrs.get('password')) or authenticate(phone_number=attrs.get('phone_number'), password=attrs.get('password'))
        if user and user.check_password(attrs.get('password')):
            attrs['email'] = user.email
        return super().validate(attrs)
    
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class PhoneVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = ['phone_number', 'verification_code', 'created_at', 'expires_at']
        read_only_fields = ['verification_code', 'created_at', 'expires_at']


class SendVerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        """Validate phone number format"""
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with country code (e.g., +234)")
        
        # Remove + and check if remaining characters are digits
        digits_only = value[1:]
        if not digits_only.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits after country code")
        
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise serializers.ValidationError("Phone number must be between 10 and 15 digits")
        
        return value


class VerifyPhoneCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    verification_code = serializers.CharField(max_length=6, min_length=6)
    
    def validate_verification_code(self, value):
        """Validate verification code format"""
        if not value.isdigit():
            raise serializers.ValidationError("Verification code must be 6 digits")
        return value