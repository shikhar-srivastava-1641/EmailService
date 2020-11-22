import pandas
import traceback

from EmailService.apis.send_mail import SendMail
from EmailService.utils.logger import Logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from EmailService.exceptions import CSVFileNotFoundException, FileTypeMismatchException
from django.conf import settings

logger = Logger(__name__)


class SendMailCSV(APIView):

    def __init__(self, **kwargs):
        """init for send mail via csv"""
        super(SendMailCSV, self).__init__(**kwargs)
        self.file = None

    def post(self, request):
        """API to send mail from CSV"""
        try:
            csv_file = request.FILES

            if csv_file:

                file = csv_file.get('file')
                file_name = csv_file.get('file').name

                file_parts = file_name.split('.')
                extension = file_parts[-1]

                if extension.lower() != "csv":
                    raise FileTypeMismatchException("File type is incorrect")

                self.file = file

                df = pandas.read_csv(self.file)
                data = df.T.apply(lambda x: x.dropna().to_dict()).tolist()

                for email_detail in data:
                    self.send_email_csv(email_detail)

                return Response({"status": "success"}, status=status.HTTP_200_OK)

            else:
                raise CSVFileNotFoundException("CSV file not found")

        except FileTypeMismatchException as e:
            logger.log("critical", {"Exception": str(e)})
            return Response({"status": "fail", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except CSVFileNotFoundException as e:
            logger.log("critical", {"Exception": str(e)})
            return Response({"status": "fail", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            traceback_msg = traceback.format_exc().splitlines()
            logger.log("critical", {"Exception": e, "Traceback": traceback_msg})

            return Response({"status": "fail", "error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def send_email_csv(email_detail):
        """Method to Send email by csv"""
        sender = settings.EMAIL_ID
        receivers = email_detail.get('receivers', '')
        cc = email_detail.get('cc', '')
        bcc = email_detail.get('bcc', '')
        subject = email_detail.get('subject', '')
        message = email_detail.get('message', '')

        send_email_obj = SendMail(
            sender=sender,
            receivers=receivers,
            cc=cc,
            bcc=bcc,
            subject=subject,
            message=message
        )

        send_email_obj.create_email_entry_in_db()
        send_email_obj.send_email()
