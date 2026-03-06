variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "news-aggregator"
}

variable "github_repo" {
  type        = string
  description = "GitHub repo in owner/name format for OIDC trust policy"
  default     = "avishek-das/news-aggregator"
}

# Fill these in before deploying ECS (Phase 1.2+)
variable "vpc_id" {
  type        = string
  description = "Existing AWS VPC ID — confirm with: aws ec2 describe-vpcs"
  default     = ""
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs for ECS tasks"
  default     = []
}

variable "public_subnet_ids" {
  type        = list(string)
  description = "Public subnet IDs for ALB"
  default     = []
}
