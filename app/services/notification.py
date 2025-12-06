from typing import List

class NotificationService:
    def send_email(self, to_email: str, subject: str, body: str):
        print(f"Mock Sending Email to {to_email}: {subject}")

    def send_sms(self, phone_number: str, message: str):
        print(f"Mock Sending SMS to {phone_number}: {message}")

notification_service = NotificationService()
