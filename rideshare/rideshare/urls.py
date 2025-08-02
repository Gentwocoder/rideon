from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import (RegisterView, CustomTokenView, ProfileView, DriverProfileView, 
                       LogoutView, LoginView, VerifyEmailView, send_verification_code,
                       verify_phone_code, phone_verification_status, ChangePasswordView,
                       ForgotPasswordView, ResetPasswordView, DashboardView, DriverDashboardView,
                       ProfileTemplateView, PhoneVerificationView, ChangePasswordPageView)
from rideon.views import RequestRideView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints
    path("api/", include("rideon.urls")),
    # path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # path(
    #     "api/schema/docs/",
    #     SpectacularSwaggerView.as_view(url_name="schema"),
    #     name="docs",
    # ),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("api/token/", CustomTokenView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile_api"),
    path("driver-profile/", DriverProfileView.as_view(), name="driver_profile"),
    path("auth/login/", LoginView.as_view(), name="login_api"),
    path("api/verify-email/<uuid:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    
    # Phone verification endpoints
    path("api/phone/send-code/", send_verification_code, name="send_verification_code"),
    path("api/phone/verify-code/", verify_phone_code, name="verify_phone_code"),
    path("api/phone/status/", phone_verification_status, name="phone_verification_status"),
    
    # Password management endpoints
    path("auth/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("auth/forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("auth/reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    
    # Frontend routes
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("driver-dashboard/", DriverDashboardView.as_view(), name="driver_dashboard"),
    path("request-ride/", RequestRideView.as_view(), name="request_ride"),
    path("my-profile/", ProfileTemplateView.as_view(), name="profile"),
    path("verify-phone/", PhoneVerificationView.as_view(), name="phone_verification"),
    path("verify-email/<uuid:token>/", TemplateView.as_view(template_name="email_verification.html"), name="email_verification"),
    path("change-password/", ChangePasswordPageView.as_view(), name="change_password_page"),
    path("forgot-password/", TemplateView.as_view(template_name="forgot_password.html"), name="forgot_password_page"),
    path("reset-password/<uuid:token>/", TemplateView.as_view(template_name="reset_password.html"), name="reset_password_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
