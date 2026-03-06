output "ecr_repository_url" {
  value       = aws_ecr_repository.backend.repository_url
  description = "ECR URL — used in GitHub Actions deploy workflow"
}

output "github_actions_role_arn" {
  value       = aws_iam_role.github_actions_deployer.arn
  description = "Add this as AWS_ROLE_ARN in GitHub repo secrets"
}

output "secret_arns" {
  value       = { for k, v in aws_secretsmanager_secret.app : k => v.arn }
  description = "Secret ARNs — reference these in ECS task definitions"
}
