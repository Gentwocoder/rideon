# Rideon - Advanced Ride Sharing Platform

A modern, full-featured ride sharing platform built with Django REST Framework and responsive frontend, featuring phone verification, real-time communication, and interactive mapping.

## 🚀 Key Features

### 🔐 Advanced User Management
- **Dual Authentication**: Email + Phone number verification with SMS OTP
- **User Types**: Support for Riders, Drivers, and Admins with role-based access
- **Email Verification**: Mandatory email verification for account activation
- **Phone Verification**: SMS-based phone number verification with Twilio integration
- **Password Security**: Enhanced password requirements with strength validation
- **Password Management**: Secure change password and forgot password features
- **Profile Management**: Comprehensive user and driver profile management
- **Driver Profiles**: Vehicle information, license management, and availability status
- **Enhanced Security**: JWT authentication with refresh token support

### 🚗 Complete Ride Management
- **Intelligent Ride Requests**: Advanced ride booking with location autocomplete
- **Google Maps Integration**: Real driving routes with traffic-aware directions
- **Interactive Mapping**: Leaflet fallback with Nigerian location database
- **Driver Matching**: Smart driver-rider matching with real-time availability
- **Ride Status Tracking**: Complete lifecycle from request to completion
- **Nigerian Naira Pricing**: Localized fare calculation (₦500 base + ₦150/km + ₦25/min)
- **Ride History**: Comprehensive ride tracking and analytics
- **Payment Options**: Cash payment system (expandable for digital payments)

### 💬 Real-Time Communication
- **Driver-Rider Messaging**: Bidirectional communication system
- **Arrival Notifications**: Automated driver arrival alerts
- **Message Types**: Support for general messages, delays, and route changes
- **Chat Interface**: Professional messaging UI with timestamps
- **Contact System**: Easy communication when drivers reach pickup location

### ⭐ Rating & Review System
- **Mutual Rating**: Both riders and drivers can rate each other
- **Category Ratings**: Punctuality, communication, cleanliness, professionalism
- **Comment System**: Optional detailed feedback
- **Rating Display**: Interactive star-based interface
- **Statistics Integration**: Average ratings in driver profiles
- **Trust Building**: Comprehensive accountability system

### 🗺️ Advanced Mapping & Location
- **Google Maps API**: Professional mapping with real route calculation
- **Places Autocomplete**: Nigerian location suggestions with smart search
- **Leaflet Fallback**: OpenStreetMap integration when Google Maps unavailable
- **Location Search**: Comprehensive Nigerian cities database (40+ locations)
- **Route Visualization**: Interactive maps with pickup/dropoff markers
- **Distance Calculation**: Accurate fare estimation based on real routes

### 📱 Enhanced Frontend Features
- **Responsive Design**: Mobile-first Bootstrap 5 interface
- **Interactive Dashboards**: Separate optimized dashboards for riders and drivers
- **Real-time Updates**: Auto-refreshing data without page reloads
- **Smart Notifications**: In-app alerts and status updates
- **Form Validation**: Comprehensive client-side and server-side validation
- **Error Handling**: User-friendly error messages with specific field feedback
- **Nigerian Localization**: Naira currency, local addresses, and phone formats

## 🛠️ Tech Stack

### Backend
- **Django 5.2.4**: Modern Python web framework
- **Django REST Framework**: Comprehensive API development
- **SimpleJWT**: JWT authentication with refresh token support
- **SQLite**: Development database with production-ready migrations
- **Custom User Model**: Email + phone based authentication
- **Twilio Integration**: SMS service for phone verification
- **Rate Limiting**: API protection and SMS abuse prevention

### Frontend
- **HTML5/CSS3/JavaScript**: Modern web standards
- **Bootstrap 5.3**: Responsive UI framework
- **Font Awesome**: Professional icons and visual elements
- **Google Maps API**: Interactive mapping and location services
- **Leaflet**: Fallback mapping solution with routing
- **Vanilla JavaScript**: Lightweight, no heavy frameworks
- **Service Worker**: PWA capabilities for offline functionality

### Third-Party Services
- **Twilio**: SMS verification and communication
- **Google Maps**: Geocoding, directions, and places API
- **OpenStreetMap**: Alternative mapping via Leaflet
- **Console Email**: Development email backend

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)
- Twilio account (for SMS features)
- Google Maps API key (for enhanced mapping)

### Installation

1. **Clone and setup the project**:
```bash
git clone https://www.github.com/gentwocoder/rideon.git
cd "Ride Sharing Project/rideshare"
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**:
Create a `.env` file in the project root:
```env
# SMS Configuration (Twilio)
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Google Maps API Key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Email Configuration
DEFAULT_FROM_EMAIL=your_email@example.com
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Development Settings
DEBUG=True
SECRET_KEY=your-secret-key
```

5. **Database Setup**:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser** (optional):
```bash
python manage.py createsuperuser
```

7. **Test SMS Service** (optional):
```bash
python manage.py test_sms +234XXXXXXXXXX
```

8. **Start the development server**:
```bash
python manage.py runserver
```

9. **Access the application**:
   - **Frontend**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/
   - **API Documentation**: http://127.0.0.1:8000/api/

## 📱 Usage Guide

### For Riders
1. **Register**: Create account at `/register/` with email and phone number
2. **Verify Email**: Check email and click verification link
3. **Verify Phone**: Enter phone number and SMS verification code
4. **Login**: Access your dashboard at `/dashboard/`
5. **Request Ride**: Use interactive map to set pickup/dropoff locations
6. **Track Ride**: Monitor real-time ride status and communicate with driver
7. **Rate Experience**: Provide feedback after ride completion

### For Drivers
1. **Register as Driver**: Select "Provide Rides" with vehicle information
2. **Complete Profile**: Add license details and vehicle specifications
3. **Verify Credentials**: Complete email and phone verification
4. **Go Online**: Toggle availability in driver dashboard
5. **Accept Rides**: View ride requests with route information
6. **Communicate**: Send arrival notifications and chat with riders
7. **Complete Rides**: Update status and collect ratings

## 🔌 API Endpoints

### Authentication & User Management
- `POST /auth/register/` - User registration with validation
- `POST /auth/login/` - JWT login with email/phone
- `POST /auth/logout/` - Token invalidation and logout
- `POST /api/token/refresh/` - Refresh JWT access token
- `GET /api/verify-email/<token>/` - Email verification
- `POST /api/send-verification-code/` - Send SMS verification
- `POST /api/verify-phone-code/` - Verify SMS code
- `GET /api/phone-verification-status/` - Check verification status
- `POST /auth/change-password/` - Change password for authenticated users
- `POST /auth/forgot-password/` - Request password reset email
- `POST /auth/reset-password/` - Reset password using token

### Profile Management
- `GET/PUT /profile/` - User profile CRUD operations
- `GET/PUT /driver-profile/` - Driver profile with vehicle details

### Ride Management
- `GET/POST /api/` - List user rides/create ride requests
- `GET /api/available/` - Available rides for drivers
- `PUT /api/{id}/accept/` - Accept ride request (drivers)
- `PUT /api/{id}/status/` - Update ride status
- `POST /api/{id}/arrival/` - Send arrival notification

### Communication
- `GET/POST /api/{ride_id}/messages/` - Ride messaging system
- `GET /api/{user_id}/ratings/` - User ratings and reviews

### Rating System
- `POST /api/{ride_id}/rate/` - Submit ride rating
- `GET /api/{ride_id}/ratings/` - View ride ratings
- `PUT /api/ratings/{id}/` - Update rating
- `DELETE /api/ratings/{id}/` - Delete rating

## 🏗️ Project Structure

```
rideshare/
├── core/                      # User management & authentication
│   ├── models.py             # CustomUser, DriverProfile, PhoneVerification
│   ├── views.py              # Auth views, phone verification
│   ├── serializers.py        # User serializers with validation
│   ├── sms_service.py        # SMS integration (Twilio, Mock)
│   └── management/commands/   # Management commands
├── rideon/                   # Ride management & communication
│   ├── models.py             # Ride, RideMessage, Rating models
│   ├── views.py              # Ride API, messaging, rating views
│   ├── serializers.py        # Ride serializers
│   └── migrations/           # Database migrations
├── templates/                # Frontend templates
│   ├── base.html             # Base template with navigation
│   ├── home.html             # Landing page with features
│   ├── register.html         # Enhanced registration with validation
│   ├── dashboard.html        # Rider dashboard with messaging
│   ├── driver_dashboard.html # Driver dashboard with earnings
│   ├── request_ride.html     # Interactive ride booking with maps
│   ├── phone_verification.html # Phone verification interface
│   ├── email_verification.html # Email verification page
│   ├── change_password.html  # Password change interface
│   ├── forgot_password.html  # Password reset request page
│   └── reset_password.html   # Password reset with token validation
├── static/                   # Static assets
│   ├── css/main.css          # Enhanced styling
│   └── js/                   # JavaScript modules
├── rideshare/                # Main project configuration
│   ├── settings.py           # Django settings with SMS/email config
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI configuration
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # This documentation
```

## 🎯 Feature Highlights

### 🔒 Security Features
- **Dual Verification**: Email + SMS verification for enhanced security
- **Rate Limiting**: Prevents SMS abuse (3 attempts per 10 minutes)
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Comprehensive validation on frontend and backend
- **Phone Format Validation**: International format enforcement (+234...)

### 🌍 Nigerian Market Focus
- **Naira Currency**: All pricing in Nigerian Naira (₦)
- **Local Locations**: 40+ Nigerian cities in location database
- **Phone Format**: Nigerian phone number validation (+234...)
- **Realistic Pricing**: Base fare ₦500, ₦150/km, ₦25/minute

### 💻 Technical Excellence
- **Responsive Design**: Works perfectly on mobile and desktop
- **Offline Capabilities**: Service worker for offline functionality
- **Error Handling**: Graceful error handling with user feedback
- **Performance**: Optimized queries and efficient data loading
- **Scalability**: Modular architecture ready for expansion

## 🧪 Testing

### Manual Testing
```bash
# Test SMS service
python manage.py test_sms +234XXXXXXXXXX

# Create test data
python manage.py shell
>>> from core.models import CustomUser
>>> user = CustomUser.objects.create_user(
...     email='test@example.com',
...     phone_number='+2341234567890',
...     password='testpass123'
... )
```

### API Testing with cURL
```bash
# Test registration
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "phone_number": "+2341234567890",
    "password": "testpass123",
    "confirm_password": "testpass123",
    "user_type": "RIDER"
  }'

# Test ride creation
curl -X POST http://127.0.0.1:8000/api/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "pickup_location": "Ikeja, Lagos",
    "pickup_latitude": 6.6018,
    "pickup_longitude": 3.3515,
    "dropoff_location": "Victoria Island, Lagos",
    "dropoff_latitude": 6.4281,
    "dropoff_longitude": 3.4219,
    "payment_method": "cash",
    "notes": "Test ride"
  }'
```

## 🔧 Configuration Options

### SMS Providers
```env
# Mock SMS (Development)
SMS_PROVIDER=mock

# Twilio (Production)
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_number

# Termii (Alternative)
SMS_PROVIDER=termii
TERMII_API_KEY=your_api_key
```

### Map Providers
```env
# Google Maps (Recommended)
GOOGLE_MAPS_API_KEY=your_api_key

# Leaflet Fallback (No API key needed)
# Automatically used when Google Maps unavailable
```

## 🚀 Production Deployment

### Environment Setup
1. **Update settings for production**:
   - Set `DEBUG=False`
   - Configure database (PostgreSQL recommended)
   - Set up proper email backend (SMTP)
   - Configure SMS provider credentials

2. **Security considerations**:
   - Use environment variables for sensitive data
   - Set up HTTPS/SSL certificates
   - Configure CORS for frontend domain
   - Set up proper database backups

3. **Performance optimizations**:
   - Configure static file serving (nginx/Apache)
   - Set up database connection pooling
   - Enable caching (Redis recommended)
   - Configure logging for monitoring

## 📊 Recent Updates (Version 2.0)

### ✅ Major Features Added
- **Phone Verification System**: Complete SMS-based verification with Twilio
- **Rating & Review System**: Mutual rating system for riders and drivers
- **Google Maps Integration**: Real-time routing and location autocomplete
- **Driver-Rider Communication**: Real-time messaging system
- **Nigerian Localization**: Currency, locations, and phone number formats
- **Enhanced Security**: Dual verification and rate limiting
- **Payment Options**: Cash payment system foundation
- **Interactive Mapping**: Dual map system (Google Maps + Leaflet fallback)

### 🔄 Improvements
- **Enhanced Error Handling**: Field-specific validation errors
- **Improved UX**: Real-time form validation and feedback
- **Better Documentation**: Comprehensive API documentation
- **Code Quality**: Modular architecture and clean code practices
- **Testing**: Comprehensive testing utilities and commands

## 🔮 Future Roadmap

### Phase 3 - Advanced Features
- **Real-time Tracking**: WebSocket integration for live location updates
- **Digital Payments**: Integration with Flutterwave, Paystack
- **Push Notifications**: Mobile app notifications
- **Advanced Analytics**: Ride patterns and user insights
- **Multi-language Support**: Hausa, Yoruba, Igbo language options

### Phase 4 - Scale & Optimization
- **Microservices Architecture**: Service decomposition
- **Mobile Apps**: React Native mobile applications
- **AI Integration**: Smart driver-rider matching algorithms
- **Business Features**: Fleet management, corporate accounts
- **Regional Expansion**: Multi-city and multi-country support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code style
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure mobile responsiveness for UI changes

## 📄 License

This project is for educational and portfolio purposes. For commercial use, ensure compliance with local ride-sharing regulations and obtain necessary licenses.

## 📞 Support & Contact

For issues, questions, or contributions:
- **GitHub Issues**: [Report bugs or request features](https://github.com/gentwocoder/rideon/issues)
- **Documentation**: [Django](https://docs.djangoproject.com/) | [DRF](https://www.django-rest-framework.org/)
- **Email**: For serious inquiries and collaborations

---

### 📈 Project Status
- **Version**: 2.0.0
- **Status**: ✅ Production Ready
- **Last Updated**: July 23, 2025
- **Core Features**: ✅ Complete with advanced functionality
- **Testing**: ✅ Comprehensive testing suite
- **Documentation**: ✅ Complete with examples
- **Security**: ✅ Production-grade security measures

**Built with ❤️ for the Nigerian ride-sharing market**