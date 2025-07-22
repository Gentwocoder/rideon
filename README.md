# Rideon - Ride Sharing Platform

A modern, full-stack ride sharing platform built with Django REST Framework and a responsive frontend.

## Features

### User Management
- **User Registration & Authentication**: Email-based registration with JWT tokens
- **User Types**: Support for Riders, Drivers, and Admins
- **Email Verification**: Mandatory email verification for account activation
- **Profile Management**: Comprehensive user and driver profile management
- **Driver Profiles**: Vehicle information, license management, and availability status

### Ride Management
- **Ride Requests**: Riders can request rides with pickup/dropoff locations
- **GPS Integration**: Location-based services with coordinate validation
- **Driver Matching**: Drivers can view and accept available ride requests
- **Real-time Status**: Track ride status from pending to completion
- **Fare Calculation**: Distance-based fare estimation with transparent pricing
- **Ride History**: Complete ride tracking and history management

### Frontend Features
- **Responsive Design**: Bootstrap-based responsive UI with modern aesthetics
- **Interactive Dashboard**: Separate dashboards for riders and drivers
- **Real-time Updates**: Auto-refreshing data and notifications
- **Progressive Web App**: Service worker for offline capabilities
- **Form Validation**: Comprehensive client-side and server-side validation
- **Error Handling**: User-friendly error messages and debugging support

## Tech Stack

### Backend
- **Django 5.2.4**: Python web framework
- **Django REST Framework**: API development with comprehensive serialization
- **SimpleJWT**: JWT authentication with refresh token support
- **SQLite**: Database (development) with migration support
- **Custom User Model**: Email-based authentication system

### Frontend
- **HTML5/CSS3/JavaScript**: Core web technologies
- **Bootstrap 5.3**: UI framework with responsive design
- **Font Awesome**: Icons and visual elements
- **Vanilla JavaScript**: No heavy frameworks, lightweight and fast
- **Service Worker**: PWA capabilities for offline functionality

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone and setup the project**:
```bash
cd "rideon/rideshare"
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Create a superuser** (optional):
```bash
python manage.py createsuperuser
```

5. **Start the development server**:
```bash
python manage.py runserver
```

6. **Access the application**:
   - Frontend: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Endpoints: http://127.0.0.1:8000/api/

## Usage Guide

### For Riders
1. **Register**: Create an account at `/register/`
2. **Verify Email**: Check your email and click the verification link
3. **Login**: Access your dashboard at `/dashboard/`
4. **Request Ride**: Click "Request Ride" and enter pickup/dropoff locations
5. **Track Ride**: Monitor ride status in your dashboard

### For Drivers
1. **Register as Driver**: Select "Provide Rides" during registration
2. **Complete Driver Profile**: Add vehicle information and license details
3. **Go Online**: Toggle availability in the driver dashboard
4. **Accept Rides**: View and accept available ride requests
5. **Complete Rides**: Update ride status through the driver interface

## API Endpoints

### Authentication
- `POST /auth/register/` - User registration with email verification
- `POST /auth/login/` - User login with JWT token generation
- `POST /auth/logout/` - User logout and token invalidation
- `POST /api/token/refresh/` - Refresh JWT access token
- `GET /api/verify-email/<token>/` - Email verification endpoint

### User Management
- `GET/PUT /profile/` - User profile management
- `GET/PUT /driver-profile/` - Driver profile management with vehicle details

### Ride Management
- `GET/POST /api/` - List user rides/create new ride requests
- `GET /api/available/` - Available rides for drivers to accept
- `PUT /api/{id}/accept/` - Accept a ride request (drivers only)
- `PUT /api/{id}/status/` - Update ride status (in_progress, completed, cancelled)

## Project Structure

```
rideshare/
├── core/                   # User management app
│   ├── models.py          # CustomUser and DriverProfile models
│   ├── views.py           # Authentication and profile views
│   ├── serializers.py     # User and profile serializers
│   ├── admin.py           # Django admin configuration
│   └── migrations/        # Database migrations
├── rideon/                # Ride management app
│   ├── models.py          # Ride and RideRequest models
│   ├── views.py           # Ride API views and logic
│   ├── serializers.py     # Ride serializers
│   ├── urls.py            # Ride URL patterns
│   └── migrations/        # Database migrations
├── rideshare/             # Main project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── templates/             # Frontend templates
│   ├── base.html          # Base template with navigation
│   ├── home.html          # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Rider dashboard
│   ├── driver_dashboard.html # Driver dashboard
│   ├── email_verification.html # Email verification page
│   └── request_ride.html  # Ride request form
├── static/                # Static assets
│   ├── css/
│   │   └── main.css       # Main stylesheet
│   └── js/
│       ├── auth.js        # Authentication utilities
│       ├── main.js        # Main JavaScript functions
│       └── sw.js          # Service worker
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
└── schema.yml             # API schema documentation
```

## Development Notes

### Recent Updates
- **✅ Ride Request Functionality**: Fixed coordinate precision issues and validation
- **✅ Email Verification**: Complete email verification system with HTML templates
- **✅ User Type Management**: Proper dashboard redirection for riders vs drivers
- **✅ Driver Profile Management**: Full CRUD operations for driver profiles
- **✅ Error Handling**: Comprehensive error handling and user feedback

### Current Limitations
1. **No real-time features**: WebSocket support not implemented
2. **Basic fare calculation**: Simple distance-based pricing
3. **No payment integration**: Payment system not implemented
4. **Mock location services**: GPS integration partially implemented
5. **SQLite database**: Production needs PostgreSQL/MySQL

### Future Enhancements
1. **Real-time notifications**: WebSocket integration for live updates
2. **Map integration**: Google Maps or Mapbox for visual ride tracking
3. **Payment processing**: Stripe or PayPal integration
4. **Advanced matching**: Algorithm-based driver-rider matching
5. **Rating system**: Comprehensive rating and review system
6. **Chat system**: In-app communication between riders and drivers
7. **Push notifications**: Mobile app notifications for ride updates

## Troubleshooting

### Common Issues

#### Ride Request Errors
- **"Ensure that there are no more than 6 decimal places"**: GPS coordinates automatically formatted to 6 decimal places
- **"Failed to request ride"**: Ensure user is logged in and has valid authentication token
- **Missing coordinates**: Use default coordinates or GPS location button for accurate positioning

#### Authentication Issues
- **Invalid credentials**: Verify email and password, ensure email is verified
- **Token expired**: Logout and login again to refresh authentication token
- **Email verification**: Check spam folder and ensure verification link hasn't expired

#### Database Issues
- **Migration errors**: Run `python manage.py migrate` to update database schema
- **Missing tables**: Ensure all migrations are applied before starting server

### Testing

#### API Testing
```bash
# Test ride creation
curl -X POST http://127.0.0.1:8000/api/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "pickup_location": "Test Location",
    "pickup_latitude": 40.712800,
    "pickup_longitude": -74.006000,
    "dropoff_location": "Test Destination",
    "dropoff_latitude": 40.758900,
    "dropoff_longitude": -73.985100,
    "notes": "Test ride"
  }'
```

#### Frontend Testing
1. Register a new user account
2. Verify email address
3. Login and access dashboard
4. Create a ride request
5. Test driver functionality with separate account

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with local regulations before deploying a ride-sharing service.

## Support

For issues and questions, please check the Django and DRF documentation:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

### Project Status
- **Version**: 1.0.0
- **Status**: Active Development
- **Last Updated**: July 12, 2025
- **Core Features**: ✅ Complete
- **Testing**: ✅ Basic functionality verified
