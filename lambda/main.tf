provider "aws" {
  region = "us-east-1"
}

# IAM role for Lambda execution
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

# Attach the Lambda basic execution role policy
resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "lambda-policy-attachment"
  roles      = [aws_iam_role.lambda_execution_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Layer for Python dependencies
resource "aws_lambda_layer_version" "python_dependencies" {
  filename   = "${path.module}/lambda_layer.zip"
  layer_name = "python-patimepluse-test-dependencies"
  compatible_runtimes = ["python3.8", "python3.9", "python3.10"]
}

# Lambda Function
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

# CloudWatch EventBridge Rule for triggering Lambda every 8 hours
resource "aws_cloudwatch_event_rule" "every_8_hours" {
  name        = "every-8-hours-rule"
  description = "Trigger Lambda every 8 hours"
  schedule_expression = "rate(8 hours)"  # Runs every 8 hours
}

# CloudWatch EventBridge Target to trigger Lambda function
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.every_8_hours.name
  target_id = "lambda-target"
  arn       = aws_lambda_function.tech_job_bot.arn
}

# Allow EventBridge to invoke Lambda function
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tech_job_bot.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_8_hours.arn
}

# Output ARNs
output "lambda_function_arn" {
  value = aws_lambda_function.tech_job_bot.arn
}

output "lambda_layer_arn" {
  value = aws_lambda_layer_version.python_dependencies.arn
}

output "event_rule_arn" {
  value = aws_cloudwatch_event_rule.every_8_hours.arn
}
