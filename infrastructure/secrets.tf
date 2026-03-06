# Secret definitions — values are set manually via AWS CLI or Console, never in Terraform
locals {
  secrets = [
    "supabase-db-url",
    "supabase-anon-key",
    "supabase-service-key",
    "gemini-api-key",
    "anthropic-api-key",
    "reddit-client-id",
    "reddit-client-secret",
  ]
}

resource "aws_secretsmanager_secret" "app" {
  for_each = toset(local.secrets)
  name     = "${var.project_name}/${each.key}"

  lifecycle {
    prevent_destroy = true
  }
}
