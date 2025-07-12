from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
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
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


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
    def get(self, request, token):
        user = get_object_or_404(CustomUser, email_verification_token=token)
        user.is_email_verified = True
        user.email_verification_token = None
        user.save()
        return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
    
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

