from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from .serializers import CustomTokenSerializer, UserSerializer, RegisterSerializer, DriverProfileSerializer, LoginSerializer
from .models import CustomUser

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        print("Registration request data:", request.data)  # Debug logging
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            return Response({
                'message': 'Registration successful! Please check your email to verify your account.',
                'user': {
                    'email': user.email,
                    'user_type': user.user_type,
                    'is_email_verified': user.is_email_verified
                },
                'status': 'success'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Registration error:", str(e))  # Debug logging
            print("Serializer errors:", serializer.errors if hasattr(serializer, 'errors') else 'No serializer errors')
            return Response({
                'message': 'Registration failed',
                'errors': serializer.errors if hasattr(serializer, 'errors') else {'detail': str(e)},
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
        serializer = self.serializer_class(request.user.profile)
        if not serializer:
            return Response({"error": "Profile not found"}, status=404)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = self.serializer_class(request.user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        request.user.profile.delete()
        return Response(status=204)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
                         "data": {"email": user.email}, "status": "success"},
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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

