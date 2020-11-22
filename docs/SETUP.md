## Setting up a local development environment

These instructions assume that the service will be 
running on MAC OS as the host operating system. 

####Prerequisites for the project:
* Python:~ v3.6
* Docker:~ v19.03.13
* docker-compose:~ v1.27.4
##
####Dependencies
All the dependencies that are required for the email
service to run:
```text
django==2.1
djangorestframework==3.8.2
requests==2.18.1
aiosmtplib==1.1.4
celery==4.2.1
ipython==7.16.1
pandas==1.1.4
```
##

The complete project is dockerized and one just need
to run the docker-compose command to make the service
up and running.

####Steps Involved:
1. Cloning the repository

    ```bash
    cd ~
    git clone https://github.com/shikhar-srivastava-1641/EmailService.git
    ``` 

2. Building the docker. This will create the docker
image and install all the required dependencies.
    ```bash
    docker-compose build
    ```

3. Make the container up and start the service. The
service will be available and accessible on 
http://localhost:8090/

    ```bash
    docker-compose up
    ```