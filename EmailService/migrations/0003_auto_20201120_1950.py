# Generated by Django 2.1 on 2020-11-20 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EmailService', '0002_auto_20201120_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='file',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='EmailService.File'),
        ),
    ]
