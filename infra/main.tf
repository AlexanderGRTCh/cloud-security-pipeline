provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "flask_server" {
ami = "ami-0c65adc9a5c1b5d7c" # Ubuntu 22.04 in Canada region
  instance_type = "t2.micro"
  key_name = "LaptopPipeProject"  

  tags = {
    Name = "FlaskSecurityDemo"
  }
}
