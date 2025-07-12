from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import RegisterView, CustomTokenView, ProfileView, DriverProfileView, LogoutView, LoginView, VerifyEmailView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("rideon.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs",
    ),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("api/token/", CustomTokenView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("driver-profile/", DriverProfileView.as_view(), name="driver_profile"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("api/verify-email/<uuid:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
