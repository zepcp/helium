# Helium app

Dependencies
-------
.env file

    SECRET_KEY="my_secret_key"

*If using postgres as database*

    DB_NAME="my_name"
    DB_HOST="my_host"
    DB_USER="my_user"
    DB_PASSWORD="my_pass"

Locally
-------
Install requirements

    brew install python3.9
    pip install -r requirements.txt

Launch

    uvicorn main:app --reload

Access

    http://localhost:8000/docs

With Docker
-------
Build docker image

    docker build -t helium-app .

Launch container

    docker run -d --name helium-container -p 80:80 helium-app

Access container

    http://0.0.0.0/docs

Useful commands

    docker start helium-container
    docker stop helium-container
    docker rm helium-container
    docker logs helium-container

    docker rm -f $(docker ps -a -q);
    docker rmi $(docker images);

On AWS
-------
Deploying image to ECR

    aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
    docker build -t helium-app .
    docker tag helium-app:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/helium-app:latest
    docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/helium-app:latest

Launching image on EC2

    ssh -i <access_key>.pem ec2-user@<ip_address>
    sudo yum install -y docker
    aws configure
 
    sudo groupadd docker
    sudo gpasswd -a ${USER} docker
    sudo service docker restart

    aws ecr get-login-password --region <region> --no-include-email
    docker login -u AWS -p .. https://<aws_account_id>.dkr.ecr.<region>.amazonaws.com

    docker pull <aws_account_id>.dkr.ecr.<region>.amazonaws.com/helium-app:latest
    docker run -d --name helium-container -p 80:80 <aws_account_id>.dkr.ecr.<region>.amazonaws.com/helium-app
