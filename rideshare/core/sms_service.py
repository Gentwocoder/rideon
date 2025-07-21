"""
SMS Service for phone number verification
This module handles sending SMS verification codes to users
"""
import logging
import requests
from django.conf import settings
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class SMSService:
    """
    SMS service for sending verification codes
    This implementation uses a mock service for development
    In production, integrate with services like Twilio, AWS SNS, or African providers like Termii
    """
    
    def __init__(self):
        # Mock settings for development
        self.enabled = getattr(settings, 'SMS_ENABLED', False)
        self.provider = getattr(settings, 'SMS_PROVIDER', 'mock')
        
        # Twilio settings (example)
        self.twilio_account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
        self.twilio_auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        self.twilio_phone_number = getattr(settings, 'TWILIO_PHONE_NUMBER', '')
        
        # Termii settings (Nigerian SMS provider)
        self.termii_api_key = getattr(settings, 'TERMII_API_KEY', '')
        self.termii_sender_id = getattr(settings, 'TERMII_SENDER_ID', 'Rideon')
    
    def send_verification_code(self, phone_number: str, code: str) -> Dict[str, any]:
        """
        Send verification code via SMS
        
        Args:
            phone_number (str): The phone number to send to
            code (str): The verification code to send
            
        Returns:
            Dict: Response with success status and message
        """
        message = f"Your Rideon verification code is: {code}. This code expires in 15 minutes. Do not share this code with anyone."
        
        if not self.enabled:
            # Mock mode for development
            logger.info(f"Mock SMS: Sending code {code} to {phone_number}")
            return {
                'success': True,
                'message': f'Mock SMS sent to {phone_number}',
                'provider': 'mock',
                'code': code  # Only for development/testing
            }
        
        if self.provider == 'twilio':
            return self._send_via_twilio(phone_number, message)
        elif self.provider == 'termii':
            return self._send_via_termii(phone_number, message)
        else:
            logger.error(f"Unknown SMS provider: {self.provider}")
            return {
                'success': False,
                'message': 'SMS service not configured',
                'provider': self.provider
            }
    
    def _send_via_twilio(self, phone_number: str, message: str) -> Dict[str, any]:
        """Send SMS via Twilio"""
        try:
            from twilio.rest import Client
            
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            message = client.messages.create(
                from_=self.twilio_phone_number,
                body=message,
                to=phone_number
            )
            
            logger.info(f"Twilio SMS sent successfully to {phone_number}, SID: {message.sid}")
            return {
                'success': True,
                'message': 'SMS sent successfully',
                'provider': 'twilio',
                'sid': message.sid
            }
            
        except Exception as e:
            logger.error(f"Twilio SMS failed for {phone_number}: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'provider': 'twilio'
            }
    
    def _send_via_termii(self, phone_number: str, message: str) -> Dict[str, any]:
        """Send SMS via Termii (African SMS provider)"""
        try:
            url = "https://api.ng.termii.com/api/sms/send"
            
            payload = {
                "to": phone_number,
                "from": self.termii_sender_id,
                "sms": message,
                "type": "plain",
                "api_key": self.termii_api_key,
                "channel": "generic"
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('message') == 'Successfully Sent':
                logger.info(f"Termii SMS sent successfully to {phone_number}")
                return {
                    'success': True,
                    'message': 'SMS sent successfully',
                    'provider': 'termii',
                    'message_id': result.get('message_id')
                }
            else:
                logger.error(f"Termii SMS failed for {phone_number}: {result}")
                return {
                    'success': False,
                    'message': f"Failed to send SMS: {result.get('message', 'Unknown error')}",
                    'provider': 'termii'
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Termii SMS request failed for {phone_number}: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'provider': 'termii'
            }
        except Exception as e:
            logger.error(f"Termii SMS failed for {phone_number}: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'provider': 'termii'
            }
    
    def send_welcome_message(self, phone_number: str, user_type: str) -> Dict[str, any]:
        """Send welcome message after successful verification"""
        if user_type.upper() == 'DRIVER':
            message = "Welcome to Rideon! Your phone number has been verified. You can now start accepting ride requests."
        else:
            message = "Welcome to Rideon! Your phone number has been verified. You can now start requesting rides."
        
        if not self.enabled:
            logger.info(f"Mock SMS: Welcome message to {phone_number}")
            return {
                'success': True,
                'message': f'Mock welcome SMS sent to {phone_number}',
                'provider': 'mock'
            }
        
        if self.provider == 'twilio':
            return self._send_via_twilio(phone_number, message)
        elif self.provider == 'termii':
            return self._send_via_termii(phone_number, message)
        else:
            return {
                'success': False,
                'message': 'SMS service not configured',
                'provider': self.provider
            }


# Global SMS service instance
sms_service = SMSService()
