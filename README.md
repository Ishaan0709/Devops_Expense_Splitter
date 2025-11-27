Smart Expense Splitter – DevOps-Based Deployment 💰🚀
This project is a Flask-based web application designed to simplify expense management and sharing between multiple users.
The core purpose of this repository is to demonstrate how a simple Python application can be deployed using end-to-end DevOps practices, including automation, containerization, infrastructure-as-code, monitoring, and CI/CD readiness.

🌐 Working Application Links (Deployment Results)
These are the actual deployment outputs generated via different methods:

AWS EC2 manual deployment
🔗 http://43.204.227.172:5000/

Terraform automated deployment
🔗 http://13.233.197.55:5000/

Docker local deployment (developer's laptop)
🔗 http://localhost:5000/

Any of these links can be used to verify the working application.

🛠 DevOps Tools Used in This Project
This project demonstrates a practical DevOps pipeline using the following tools:

📱 Application Layer
Flask (Python web framework)

HTML / CSS templates

Python virtual environment

🔄 Version Control & Testing
Git and GitHub – code management, collaboration

PyTest – verifies app stability before deployment

GitHub Actions CI – automatically runs tests on every push

📦 Containerization
Docker – packages the application into a reusable container

DockerHub – hosts the container image

☁ Cloud Deployment
AWS EC2 – manual deployment to a public server

AWS CloudWatch – resource-level monitoring

🏗 Infrastructure as Code
Terraform – creates and configures EC2 instance automatically

📊 Monitoring
Shell script for health checks

AWS CloudWatch metrics

🔁 CI/CD (Future Scope)
Jenkins – containerized on Docker, credentials configured for future automation

📋 How DevOps Workflow Works in This Project
Code written locally (Flask app)

Git commit + GitHub push

PyTest ensures app is stable

GitHub Actions runs automated tests (CI)

Docker image is built and pushed to DockerHub

AWS EC2 used for manual deployment

Terraform used to deploy automatically (Infra-as-Code)

Health check script + CloudWatch for monitoring

Jenkins prepared for future CI/CD pipeline

This is a complete SDLC workflow implemented using DevOps procedures.

🐳 Key Docker Commands (Can Be Run on Any Laptop)
bash
# Build Docker image
docker build -t expense-tracker-app .

# Run container locally
docker run -d -p 5000:5000 --name expense-local expense-tracker-app

# Pull the image directly from DockerHub
docker run -d -p 5000:5000 ishaan0709dev/expense-tracker-app:latest

# Check running containers
docker ps
☁ Manual Deployment on AWS EC2 (Second Link Above)
bash
ssh -i "ishaan-key.pem" ec2-user@43.204.227.172

docker pull ishaan0709dev/expense-tracker-app:latest
docker run -d -p 5000:5000 --name expense-hub ishaan0709dev/expense-tracker-app:latest
🏗 Terraform-Based Automated Deployment (First Link Above)
bash
cd terraform/
terraform init
terraform plan
terraform apply
After successful apply, Terraform returned the following:

text
public_ip  = "13.233.197.55"
public_dns = "ec2-13-233-197-55.ap-south-1.compute.amazonaws.com"
The Flask application went live automatically, without manual EC2 setup.

📊 Monitoring (Health Check Script)
bash
#!/bin/bash
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")

if [ "$STATUS" = "200" ]; then
  echo "$(date) - OK ($STATUS)" >> health.log
else
  echo "$(date) - ERROR ($STATUS)" >> health.log
fi
To test monitoring:

bash
./monitoring/health_check.sh
cat health.log
AWS CloudWatch also provides CPU / network / uptime metrics automatically for the EC2 instance.

⚙ Jenkins Setup (Docker-Based)
bash
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
Plugins Installed:

GitHub Integration

Docker Pipeline

Terraform Wrapper

Credentials Binding

Pipeline: Groovy Libraries

Credentials added for:

DockerHub

GitHub

OpenAI API Key (optional for future ML-based features)

👥 Team Members
Final Project Presentation by:

Delphi Gupta – 102315027

Ishaan Sharma – 102303795

Jyotika Mittal – 102303722

Saksham Tiwari – 102303695

Srishti Jain – 102316080
