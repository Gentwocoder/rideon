from rest_framework import serializers
from .models import CustomUser, DriverProfile
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
        read_only_fields = ['id', 'username', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'password']

        def create(self, validated_data):
            user = CustomUser.objects.create_user(**validated_data)
            verification_url = f"http://127.0.0.1/api/verify-email/{user.email_verification_token}"
            send_mail(
                subject="Email Verification",
                message=f"Please click the link to verify your email: {verification_url}",
                from_email="adetoyese0511@gmail.com",
                recipient_list=[user.email],
            )
            user.set_password(validated_data['password'])
            user.save()
            
            return user
        
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