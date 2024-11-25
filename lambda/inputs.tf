variable "aws_region" {
  default = "us-east-1"
  description = "AWS region for Lambda deployment."
}

variable "lambda_name" {
  default = "PartTimePulse"
  description = "Name of the Lambda function."
}
