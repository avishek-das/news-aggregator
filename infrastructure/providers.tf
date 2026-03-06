terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state — bootstrap S3 bucket + DynamoDB table first:
  # aws s3 mb s3://news-aggregator-terraform-state --region us-east-1
  # aws s3api put-bucket-versioning --bucket news-aggregator-terraform-state \
  #   --versioning-configuration Status=Enabled
  # aws dynamodb create-table --table-name news-aggregator-terraform-locks \
  #   --attribute-definitions AttributeName=LockID,AttributeType=S \
  #   --key-schema AttributeName=LockID,KeyType=HASH \
  #   --billing-mode PAY_PER_REQUEST --region us-east-1
  backend "s3" {
    bucket         = "news-aggregator-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "news-aggregator-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = "production"
      ManagedBy   = "terraform"
    }
  }
}

data "aws_caller_identity" "current" {}
