provider "aws" {
  region = "us-east-1"  # Adjust as per your requirements
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      }
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "lambda-policy-attachment"
  roles      = [aws_iam_role.lambda_execution_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_layer_version" "python_dependencies" {
  filename   = "${path.module}/lambda_layer.zip"
  layer_name = "python-patimepluse-test-dependencies"
  compatible_runtimes = ["python3.8", "python3.9", "python3.10"]
}

resource "aws_lambda_function" "tech_job_bot" {
  filename         = "${path.module}/application.zip"
  function_name    = "PartTimePulse"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "main.lambda_handler"
  runtime          = "python3.9"
  layers           = [aws_lambda_layer_version.python_dependencies.arn]
  environment {
    variables = {
      LOG_LEVEL = "INFO"
    }
  }
  timeout          = 30
}

output "lambda_function_arn" {
  value = aws_lambda_function.tech_job_bot.arn
}

output "lambda_layer_arn" {
  value = aws_lambda_layer_version.python_dependencies.arn
}
