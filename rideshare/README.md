# Rideon - Ride Sharing Platform

A modern, full-stack ride sharing platform built with Django REST Framework and a responsive frontend.

## Features

### User Management
- **User Registration & Authentication**: Email-based registration with JWT tokens
- **User Types**: Support for Riders, Drivers, and Admins
- **Email Verification**: Mandatory email verification for account activation
- **Profile Management**: Comprehensive user and driver profile management

### Ride Management
- **Ride Requests**: Riders can request rides with pickup/dropoff locations
- **Driver Matching**: Drivers can view and accept available ride requests
- **Real-time Status**: Track ride status from pending to completion
- **Fare Calculation**: Basic fare estimation based on distance

### Frontend Features
- **Responsive Design**: Bootstrap-based responsive UI
- **Interactive Dashboard**: Separate dashboards for riders and drivers
- **Real-time Updates**: Auto-refreshing data and notifications
- **Progressive Web App**: Service worker for offline capabilities

## Tech Stack

### Backend
- **Django 5.2.4**: Python web framework
- **Django REST Framework**: API development
- **SimpleJWT**: JWT authentication
- **drf-spectacular**: API documentation (Swagger)
- **SQLite**: Database (development)

### Frontend
- **HTML5/CSS3/JavaScript**: Core web technologies
- **Bootstrap 5.3**: UI framework
- **Font Awesome**: Icons
- **Vanilla JavaScript**: No heavy frameworks, lightweight and fast

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone and setup the project**:
```bash
cd "/home/gentle/Documents/Ride Sharing Project/rideshare/backend"
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
   - API Documentation: http://127.0.0.1:8000/api/schema/docs/
   - Admin Panel: http://127.0.0.1:8000/admin/

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
- `POST /auth/register/` - User registration
- `POST /auth/login/` - User login
- `POST /auth/logout/` - User logout
- `POST /api/token/refresh/` - Refresh JWT token

### User Management
- `GET/PUT /profile/` - User profile management
- `GET/PUT/POST/DELETE /driver-profile/` - Driver profile management

### Ride Management
- `GET/POST /api/` - List/create rides
- `GET /api/available/` - Available rides for drivers
- `PUT /api/{id}/accept/` - Accept a ride request
- `PUT /api/{id}/status/` - Update ride status

## Project Structure

```
backend/
├── core/                   # User management app
│   ├── models.py          # User and driver profile models
│   ├── views.py           # Authentication views
│   ├── serializers.py     # API serializers
│   └── migrations/        # Database migrations
├── rideon/                # Ride management app
│   ├── models.py          # Ride and request models
│   ├── views.py           # Ride API views
│   ├── serializers.py     # Ride serializers
│   └── urls.py            # Ride URL patterns
├── rideshare/             # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/             # Frontend templates
│   ├── base.html          # Base template
│   ├── home.html          # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Rider dashboard
│   ├── driver_dashboard.html # Driver dashboard
│   ├── request_ride.html  # Ride request form
│   └── profile.html       # User profile page
├── static/                # Static assets
│   ├── css/
│   │   └── main.css       # Main stylesheet
│   └── js/
│       ├── auth.js        # Authentication utilities
│       ├── main.js        # Main JavaScript functions
│       └── sw.js          # Service worker
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Development Notes

### Current Limitations
1. **No real-time features**: WebSocket support not implemented
2. **Basic fare calculation**: Simple distance-based pricing
3. **No payment integration**: Payment system not implemented
4. **Mock location services**: GPS integration not implemented
5. **SQLite database**: Production needs PostgreSQL/MySQL

### Future Enhancements
1. **Real-time notifications**: WebSocket integration
2. **Map integration**: Google Maps or Mapbox
3. **Payment processing**: Stripe or PayPal integration
4. **Advanced matching**: Algorithm-based driver-rider matching
5. **Rating system**: Comprehensive rating and review system
6. **Chat system**: In-app communication between riders and drivers

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
