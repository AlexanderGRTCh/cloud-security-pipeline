# Configure the AWS provider and set region (us-west-2 = Oregon)
provider "aws" {
  region = "us-west-2"
}

# Create a security group for the Flask server
resource "aws_security_group" "flask_sg" {
  name        = "flask_sg"                               # Name of the security group
  description = "Allow SSH and Flask app traffic"  



  # Allow SSH (port 22) from anywhere (insecure, for demo/dev only)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow Flask app (port 5000) from anywhere (change for production!)
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic (default)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"                # -1 = all protocols
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create the EC2 server (Ubuntu 22.04, t2.micro)
resource "aws_instance" "flask_server" {
  ami           = "ami-0c65adc9a5c1b5d7c"             # Ubuntu 22.04 AMI in us-west-2
  instance_type = "t2.micro"                          # Free tier EC2 size
  key_name      = "LaptopPipeProject2"                # AWS key pair for SSH
  security_groups = [aws_security_group.flask_sg.name]# Attach security group

  tags = {
    Name = "FlaskSecurityDemo"                        # Name tag for AWS console
  }
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name


  # Automate Docker install after first boot
  user_data = <<-EOF
    #!/bin/bash
    sudo apt-get update -y                           # Update package lists
    sudo apt-get install -y docker.io                # Install Docker automatically
  EOF
}


# Output the public IP
output "public_ip" {
  value = aws_instance.flask_server.public_ip
}
