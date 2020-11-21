from django.db import models


class Files(models.Model):
    """Stores files information"""
    file_name = models.CharField(max_length=50)
    file_path = models.FilePathField(path='/EmailService/EmailService/static/uploaded_files/')

    objects = models.Manager

    class Meta:
        db_table = "email_file"


class Email(models.Model):
    """Email service model

    - Setting Receiver, cc and bcc as char_fields...
      as it will reduce the joins and improve performance...
      and since we do not want per user basis analysis.
    """
    sender = models.EmailField(max_length=30)
    receivers = models.CharField(max_length=100)
    cc = models.CharField(max_length=100, null=True)
    bcc = models.CharField(max_length=100, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    file = models.ForeignKey(Files, on_delete=models.CASCADE, default=None, null=True)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager

    class Meta:
        db_table = "email_service"
