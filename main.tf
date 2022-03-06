provider "aws" {
  region = "eu-west-1"
  profile = "PowerUserAccess"
}

resource "aws_iam_role" "deploy_role" {
  name = "ecr-deploy-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "build.apprunner.amazonaws.com"
        }
      }
    ]
  })
}
resource "aws_iam_role_policy_attachment" "deploy_role_policy_attachment" {
  role       = aws_iam_role.deploy_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

resource "aws_iam_role" "instance_role" {
  name = "ecr-instance-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "tasks.apprunner.amazonaws.com"
        }
      }
    ]
  })
}
locals {
  instance_role_name = aws_iam_role.instance_role.name
}

resource "aws_apprunner_service" "demo-project-overview" {
  service_name = "demo-projects-overview"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.deploy_role.arn
    }
    image_repository {
      image_identifier      = "projects-overview:latest"
      image_repository_type = "ECR"
    }
  }
  instance_configuration {
    instance_role_arn = aws_iam_role.instance_role.arn
  }
  tags = {
    Name = "example-apprunner-service"
  }
}

