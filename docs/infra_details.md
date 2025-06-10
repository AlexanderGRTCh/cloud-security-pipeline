# Infrastructure Details

This project provisions and manages its AWS resources using Terraform, following infrastructure-as-code (IaC) best practices for repeatable and secure cloud deployments.

## Overview of AWS Resources

- **EC2 Instance**:  
  The core compute resource that runs the Dockerized Flask application. It is provisioned with a security group for controlled access and uses an SSH key for secure administration.

- **Security Group**:  
  Acts as a virtual firewall for the EC2 instance. The security group is configured to allow only essential inbound traffic:
    - Port 22 (SSH) – for secure remote management.
    - Port 5000 (Flask) – for external access to the web application.
  All other inbound ports are blocked by default.

## Terraform File Structure

- **infra/main.tf**:  
  The primary Terraform configuration file, which defines:
    - AWS provider settings (region, credentials)
    - EC2 instance resource (AMI, instance type, SSH key association)
    - Security group resource (inbound rules for ports 22 and 5000)
    - Outputs for the instance public IP and other important values

- **infra/variables.tf** (optional):  
  Stores reusable variables for the infrastructure, such as instance type or region.

- **infra/outputs.tf** (optional):  
  Defines which values Terraform will output after applying, such as the EC2 public IP.

## Deployment Workflow

1. Initialize and apply Terraform:
    - cd infra
    - terraform init
    - terraform apply

2. Terraform provisions the EC2 instance and security group automatically, requiring no manual steps in the AWS Console.

3. The public IP output from Terraform is used as the deployment target in the CI/CD pipeline and for SSH access.

## Security Practices

- Only required ports are open (22, 5000).
- The SSH key is never stored in code—managed securely via GitHub Actions secrets.
- Security group rules can be easily audited and changed via code.

## Customization

- To allow a different app port, add a new ingress rule in main.tf and adjust the Flask app and CI/CD pipeline.
- To restrict SSH access to a specific IP or CIDR, modify the security group rule in main.tf accordingly.

## Reference

See main.tf for exact resource definitions and security group rule syntax.
