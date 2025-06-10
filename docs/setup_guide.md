# Setup Guide

This guide explains how to set up and deploy the Cloud Security Pipeline project from scratch.

## Prerequisites

- AWS account with programmatic access (IAM user or role)
- Docker Desktop (latest version)
- Terraform (latest version)
- Python 3.x
- Git (with Git Bash or similar terminal)

## 1. Clone the Repository

Clone the repository to your local machine:
git clone <https://github.com/AlexanderGRTCh/cloud-security-pipeline>
cd cloud-security-pipeline

## 2. Configure AWS Credentials

You need AWS credentials on your machine for Terraform to provision AWS resources.

Using AWS CLI:
aws configure
(Enter your AWS Access Key ID, Secret Access Key, region, and output format when prompted.)

Or manually create the credentials file at ~/.aws/credentials:
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = YOUR_REGION

## 3. Set Up Infrastructure with Terraform

Provision AWS resources (EC2, Security Group) with Terraform:
cd infra
terraform init
terraform apply
(Review and approve the plan when prompted. Note the public IP address of the EC2 instance created.)

## 4. Configure GitHub Actions Secrets

To enable automated deployments, add the following secrets to your GitHub repository (Settings > Secrets and variables > Actions):
- EC2_SSH_KEY — contents of your EC2 private key (.pem file)
- EC2_USER — EC2 username (usually ubuntu)
- EC2_HOST — EC2 instance public IP

## 5. Deploy via CI/CD Pipeline

Trigger deployment by making any change and pushing to the main branch:
git add .
git commit -m "Trigger CI/CD deployment"
git push
(This starts the automated GitHub Actions pipeline, runs security scans, and deploys your app to EC2. Monitor progress in the Actions tab of your GitHub repository.)

## 6. Optional: Local Testing

Test the app locally before deployment.

Run Flask app directly:
cd app
python app.py

Build and run the Docker container locally:
docker build -t flask_app .
docker run -d --name flask_app -p 5000:5000 flask_app

(Access the app at http://localhost:5000.)

## 7. Troubleshooting

For common issues and solutions, see troubleshooting.md.

## 8. Port Tester Script

A Python script is included at scripts/port_tester.py to verify that only the necessary ports (22 for SSH, 5000 for Flask) are open on your EC2 instance.  
You can run it from your local machine to confirm your security group configuration:

python scripts/port_tester.py

(Adjust the script or ports as needed for your environment.)
