// Terraform config for DevOps Expense Tracker
// Creates: Security Group + EC2 instance + runs Docker container

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# --- Use default VPC (so we don't create new networking) ---
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}


# --- Security Group: SSH(22), HTTP(80), Flask(5000) ---
resource "aws_security_group" "expense_sg" {
  name        = "expense-tracker-sg"
  description = "Allow SSH, HTTP, and Flask port"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "expense-tracker-sg"
  }
}

# --- AMI: latest Amazon Linux 2023 in this region ---
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# --- EC2 instance ---
resource "aws_instance" "expense_server" {
  ami                    = data.aws_ami.amazon_linux_2023.id
  instance_type          = "t3.micro"  # CHANGED: t2.micro → t3.micro
  subnet_id              = data.aws_subnets.default.ids[0]
  vpc_security_group_ids = [aws_security_group.expense_sg.id]
  key_name               = var.key_name
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ec2-user

              docker pull ${var.docker_image}
              docker run -d -p 5000:5000 --name expense-from-terraform ${var.docker_image}
              EOF

  tags = {
    Name = "ExpenseTracker-From-Terraform"
  }
}

# --- Outputs to see IP in terminal ---
output "public_ip" {
  value = aws_instance.expense_server.public_ip
}

output "public_dns" {
  value = aws_instance.expense_server.public_dns
}