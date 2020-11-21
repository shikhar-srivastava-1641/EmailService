import asyncio
import aiosmtplib
import traceback
import datetime
from django.conf import settings
from rest_framework.views import APIView
from django.core.files import File
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.shortcuts import redirect
from EmailService.utils.logger import Logger
from EmailService.model import Email, Files

logger = Logger(__name__)


class SendMail(APIView):

    def __init__(self, sender=None, receivers=None, cc=None, bcc=None, subject=None, message=None, **kwargs):
        """Init for SendMail"""
        super(SendMail, self).__init__(**kwargs)

        self.sender = sender
        self.receivers = receivers
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.message = message
        self.file_name = None
        self.file_path = None

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def post(self, request):
        """API to send emails

        :param request:
        :return:
        """
        req_data = request.POST
        uploaded_files = request.FILES

        logger.log("info", req_data)
        logger.log("info", uploaded_files)

        try:
            self.sender = req_data['from']
            self.receivers = req_data['to']
            self.cc = req_data['cc']
            self.bcc = req_data['bcc']
            self.subject = req_data['subject']
            self.message = req_data['body']

            if uploaded_files:
                self.process_files(uploaded_files)

            email_obj = self.create_email_entry_in_db()
            self.send_email()

            email_obj.is_success = True
            email_obj.save()

            return redirect(F'http://{settings.HOST}/?alert_visible=True&success=True')

        except Exception as e:

            traceback_msg = traceback.format_exc().splitlines()
            logger.log("critical", {"Exception": e, "Traceback": traceback_msg})

            return redirect(F'http://{settings.HOST}/?alert_visible=True&success=False')

    def create_email_entry_in_db(self):
        """Create DB entry for the email"""

        file_obj = None
        if self.file_name:
            file_obj = Files.objects.create(
                file_name=self.file_name,
                file_path=self.file_path
            )

        email_obj = Email.objects.create(
            sender=self.sender,
            receivers=self.receivers,
            cc=self.cc,
            bcc=self.bcc,
            subject=self.subject,
            message=self.message,
            file=file_obj
        )

        return email_obj

    def process_files(self, uploaded_files):
        """Process files"""
        f_name = uploaded_files['file'].name
        file = uploaded_files['file']

        # Upload the file to S3
        self.file_name = f_name
        self.file_path = SendMail.upload_file_to_s3(file, f_name)

    @staticmethod
    def upload_file_to_s3(file, filename):
        """Uploads files to s3"""
        file_parts = filename.split('.')

        extension = file_parts[-1]
        filename = '.'.join(file_parts[:-1])
        date_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        file_path = F'/EmailService/EmailService/static/uploaded_files/{filename}_{date_now}.{extension}'
        logger.log("info", [filename, date_now, extension, file_path])

        # Since s3 is not present we will save it to local storage
        with open(file_path, 'wb') as f:
            my_file = File(f)
            my_file.write(file.read())

        return file_path

    def send_email(self):
        """Method to send emails

        :return:
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.receivers
        msg['Subject'] = self.subject
        if self.cc:
            msg['Cc'] = self.cc
        if self.bcc:
            msg['Bcc'] = self.bcc

        msg.attach(MIMEText(self.message, 'plain'))

        if self.file_name and self.file_path:
            attachment = open(self.file_path, "rb")

            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % self.file_name)
            msg.attach(p)

        logger.log("info", ["Email details", self.sender, self.receivers, self.subject, self.message])

        self.loop.run_until_complete(self.send_email_to_all_receivers(msg))

    async def send_email_to_all_receivers(self, msg):

        # G-mail config for SSL
        host = "smtp.gmail.com"
        port = 465
        password = settings.EMAIL_PASS

        smtp = aiosmtplib.SMTP(hostname=host, port=port, use_tls=True)
        await smtp.connect()
        await smtp.login(self.sender, password)
        await smtp.send_message(msg)
        await smtp.quit()
