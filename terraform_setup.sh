#!/bin/bash

# Exit on any error
set -e

# Check if the user passed the action (up or down)
ACTION=$1

if [ -z "$ACTION" ]; then
    echo "Please provide an action: 'up' to create resources, 'down' to destroy resources."
    exit 1
fi

# Initialize Terraform
initialize_terraform() {
    echo "Initializing Terraform..."
    terraform init
}

# Plan Terraform changes
plan_terraform() {
    echo "Planning Terraform changes..."
    terraform plan
}

# Apply Terraform changes
apply_terraform() {
    echo "Applying Terraform configuration..."
    terraform apply -auto-approve
}

# Destroy Terraform resources
destroy_terraform() {
    echo "Destroying Terraform resources..."
    terraform destroy -auto-approve
}

# Bring up the resources (apply)
if [ "$ACTION" == "up" ]; then
    initialize_terraform
    plan_terraform
    apply_terraform
    echo "Terraform infrastructure has been set up successfully."

# Tear down the resources (destroy)
elif [ "$ACTION" == "down" ]; then
    destroy_terraform
    echo "Terraform infrastructure has been destroyed successfully."

else
    echo "Invalid action. Use 'up' to create or 'down' to destroy resources."
    exit 1
fi
