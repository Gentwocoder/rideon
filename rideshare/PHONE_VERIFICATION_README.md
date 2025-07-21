# Phone Verification System - Setup Guide

This guide will help you set up and use the phone verification system for both drivers and riders in the RideOn platform.

## Overview

The phone verification system provides:
- SMS-based phone number verification
- Support for multiple SMS providers (Mock, Twilio, Termii)
- Rate limiting and security features
- Dashboard integration for user prompts
- Complete API endpoints for verification workflow

## Setup Instructions

### 1. Environment Configuration

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your preferred SMS provider configuration:

#### For Development (Mock SMS):
```
SMS_PROVIDER=mock
```

#### For Production with Twilio:
```
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

#### For Production with Termii:
```
SMS_PROVIDER=termii
TERMII_API_KEY=your_api_key
TERMII_SENDER_ID=RideOn
```

### 2. Database Migration

Apply the phone verification model migration:
```bash
python manage.py migrate
```

### 3. Testing the SMS Service

Test your SMS configuration:
```bash
# Test with mock provider (development)
python manage.py test_sms +1234567890

# Test with custom message
python manage.py test_sms +1234567890 --message "Hello from RideOn!"
```

## Usage Guide

### For Users (Riders and Drivers)

1. **Access Phone Verification**:
   - Login to your dashboard
   - If your phone number is not verified, you'll see a verification alert
   - Click "Verify Phone Number" to start the process

2. **Verification Process**:
   - Enter your phone number
   - Click "Send Verification Code"
   - Check your SMS for the 6-digit code
   - Enter the code within 10 minutes
   - Complete verification

3. **Features**:
   - Automatic code expiry (10 minutes)
   - Rate limiting (3 attempts per verification)
   - Resend code option with cooldown
   - Real-time validation

### For Developers

#### API Endpoints

1. **Send Verification Code**:
```
POST /api/send-verification-code/
{
    "phone_number": "+1234567890"
}
```

2. **Verify Phone Code**:
```
POST /api/verify-phone-code/
{
    "phone_number": "+1234567890",
    "code": "123456"
}
```

3. **Check Verification Status**:
```
GET /api/phone-verification-status/
```

#### Frontend Integration

Access the verification page at:
```
/phone-verification/
```

The page includes:
- Step-by-step verification UI
- Real-time validation
- Countdown timers
- Success/error handling

## SMS Provider Setup

### Twilio Setup

1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token from the console
3. Purchase a phone number
4. Add credentials to your `.env` file

### Termii Setup (African SMS Provider)

1. Sign up at [Termii](https://www.termii.com/)
2. Get your API key from the dashboard
3. Set up a sender ID
4. Add credentials to your `.env` file

## Security Features

- **Rate Limiting**: Max 3 verification attempts per phone number
- **Code Expiry**: Verification codes expire after 10 minutes
- **Attempt Tracking**: System tracks failed attempts
- **Input Validation**: Phone number format validation
- **Authentication**: Requires user login for verification

## Configuration Options

In `settings.py`:

```python
# Phone Verification Settings
PHONE_VERIFICATION_CODE_LENGTH = 6          # Length of verification code
PHONE_VERIFICATION_CODE_EXPIRY_MINUTES = 10 # Code expiry time
PHONE_VERIFICATION_MAX_ATTEMPTS = 3         # Max verification attempts
```

## Troubleshooting

### Common Issues

1. **SMS Not Received**:
   - Check phone number format (+country_code)
   - Verify SMS provider credentials
   - Check provider account balance/credits

2. **Code Expired**:
   - Codes expire after 10 minutes
   - Request a new verification code

3. **Too Many Attempts**:
   - Wait before trying again
   - Contact support if needed

### Debug Mode

In development, with `SMS_PROVIDER=mock`, verification codes are logged to the console:
```
Mock SMS to +1234567890: Your RideOn verification code is: 123456
```

## Production Considerations

1. **SMS Credits**: Monitor your SMS provider account balance
2. **Rate Limiting**: Consider implementing additional rate limiting for production
3. **Phone Number Validation**: Implement stricter phone number validation
4. **Logging**: Set up proper logging for SMS delivery status
5. **Monitoring**: Monitor verification success rates

## Support

For issues or questions about the phone verification system:
1. Check the troubleshooting section above
2. Review SMS provider documentation
3. Check Django logs for error messages
4. Test with the provided management command

## API Documentation

The phone verification system integrates with the existing authentication system and provides RESTful endpoints for all verification operations. All endpoints require authentication except for the verification status check which uses the current user's session.
