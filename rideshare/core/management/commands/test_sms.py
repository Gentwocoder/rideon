from django.core.management.base import BaseCommand
from core.sms_service import SMSService


class Command(BaseCommand):
    help = 'Test SMS service by sending a test message'

    def add_arguments(self, parser):
        parser.add_argument('phone_number', type=str, help='Phone number to send test SMS to')
        parser.add_argument('--message', type=str, default='This is a test message from RideOn SMS service.', 
                          help='Custom message to send')

    def handle(self, *args, **options):
        phone_number = options['phone_number']
        message = options['message']
        
        self.stdout.write(f'Sending test SMS to {phone_number}...')
        
        sms_service = SMSService()
        
        try:
            success = sms_service.send_verification_code(phone_number, message)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ SMS sent successfully to {phone_number}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send SMS to {phone_number}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error sending SMS: {str(e)}')
            )
