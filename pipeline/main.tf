provider "aws" {
access_key = var.AWS_ACCESS_KEY_ID
secret_key = var.AWS_SECRET_ACCESS_KEY
region = "eu-west-2"
}

#security group
resource "aws_security_group" "c14-gem-sg" {
  name        = "example-security-group"
  description = "Example security group"
  vpc_id      = "vpc-0344763624ac09cb6" ##change this to your VCP ID
  
  #inbound
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [aws_security_group.c14-gem-sg.id]
  }
    #protocol - ssh
    ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["YOUR_IP_ADDRESS/32"] 
  }
  #outbound
  egress {
    from_port   = 0 
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }
}

#subnet
data "aws_subnet" "vpc-subnet-c14" {
  filter {
    name   = "tag:Name"
    values = ["c14-public-subnet-1"] // Name tag of the subnet
  }
}

data "aws_key_pair" "c14-trainee-gem-lo" {
  key_name = "c14-trainee-gem-lo"
}

#previous workshop - aws_instance" "c14-gem-workshopwk7-ec2
resource "aws_instance" "c14-gem-museumdb-ec2" {
    ami = "ami-0acc77abdfc7ed5a6"
    instance_type = "t3.micro"
    associate_public_ip_address = true
    subnet_id     = data.aws_subnet.vpc-subnet-c14.id 
    
    vpc_security_group_ids = [aws_security_group.c14-gem-sg.id]

    key_name = data.aws_key_pair.c14-trainee-gem-lo.key_name

    tags = {
        Name = "c14-gem-museumdb-ec2"
    }
}


# #RDS instance
resource "aws_db_instance" "c14-gem-rds" {
  allocated_storage           = 10
  db_name                     = "postgres"
  identifier                  = "c14-gem-museumdb-tf"
  engine                      = "postgres"
  engine_version              = "16.2"
  instance_class              = "db.t3.micro"
  publicly_accessible         = false
  performance_insights_enabled = false
  skip_final_snapshot         = true
  db_subnet_group_name        = "c14-public-subnet-group"
  vpc_security_group_ids      = [aws_security_group.c14-gem-sg.id]
  username                    = var.DB_USERNAME
  password                    = var.DB_PASSWORD    
}


