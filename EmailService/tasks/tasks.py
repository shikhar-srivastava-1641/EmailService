from datetime import timedelta
from celery.task import periodic_task
from django.contrib.auth.models import User
from EmailService.apis.send_mail import SendMail
from EmailService.utils.email_utils import EmailUtils
from EmailService.utils.logger import Logger

TEST_EMAIL_ID = "test.testing.1150@gmail.com"
logger = Logger(__name__)


@periodic_task(run_every=timedelta(minutes=5))
def send_email_stats():
    """Send email statistics"""
    admin_email_set = set()

    admin_users = User.objects.all()
    for user in admin_users:
        admin_email_set.add(user.email)

    logger.log("info", admin_email_set)

    email_report = EmailUtils.generate_email_report()
    logger.log("info", email_report)

    subject = email_report['subject']
    message = email_report['body']

    send_email_obj = SendMail(
        sender=TEST_EMAIL_ID,
        receivers=",".join(list(admin_email_set)),
        subject=subject,
        message=message
    )

    send_email_obj.send_email()
