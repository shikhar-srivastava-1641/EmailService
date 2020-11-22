from datetime import datetime, timedelta
from EmailService.model import Email


class EmailUtils:

    @staticmethod
    def generate_email_report(duration_in_min=30):
        """Generates reports"""

        time_threshold = datetime.now() - timedelta(hours=5)
        emails = Email.objects.filter(created_at__gte=time_threshold)

        email_counts = emails.count()

        message = F"Total emails received in past {duration_in_min}mins: {email_counts}\n\n"
        message += "\n\n".join(
            [F"From: {email.sender}\n"
             F"To: {email.receivers}\n"
             F"Cc: {email.cc}\n"
             F"Bcc: {email.bcc}\n"
             F"Subject: {email.subject}\n"
             F"Message: {email.message}\n"
             F"Timestamp: {datetime.strftime(email.created_at, '%Y-%m-%d %H:%M')}" for email in emails])

        email_report = {
            "subject": "EMAIL Report: Hourly",
            "body": message
        }

        return email_report
