FROM python:3.6

WORKDIR /EmailService

COPY ./requirements.txt /EmailService/requirements.txt
RUN pip3.6 install -r requirements.txt

COPY ./ /EmailService

CMD ["python3.6", "manage.py", "runserver", "0.0.0.0:8090"]
