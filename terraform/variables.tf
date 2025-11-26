variable "aws_region" {
  description = "AWS region to create resources in"
  default     = "ap-south-1"   # Mumbai region
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"    # Free tier eligible
}

variable "key_name" {
  description = "Key pair name for SSH"
  default     = "ishaan-key" # SAME JISKA PEM FILE HAI
}

variable "docker_image" {
  description = "Docker image to run on EC2"
  default     = "ishaan0709dev/expense-tracker-app:latest"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "Subnet CIDR block"
  default     = "10.0.1.0/24"
}
