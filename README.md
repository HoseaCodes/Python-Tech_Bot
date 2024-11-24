### AWS Lambda Deployment with Terraform

This guide outlines the setup for deploying an AWS Lambda function and a Lambda Layer using Terraform.

---

### Directory Structure

```plaintext
lambda/
├── main.tf                  # Terraform configuration
├── inputs.tf                # Inputs file for variables
├── outputs.tf               # Outputs file for Terraform
├── application.zip          # Packaged Lambda function
├── lambda_layer.zip         # Packaged Lambda layer
├── layer_requirements.txt   # Python dependencies for the layer
├── .gitignore               # Files and directories to ignore in Git
├── README.md                # Documentation
```

---

### Packaging Instructions

#### **Create Layer ZIP**
To build the Lambda Layer package:

1. Install dependencies and package them:
   ```bash
   cd lambda/part_time_pulse
   ./build.sh
   ```

#### **Create Function ZIP**
To package the Lambda function:

1. Zip the Python code (excluding dependencies):
   ```bash
   cd lambda/part_time_pulse
   ./build_app.sh
   ```

---

### Deployment Steps

1. **Initialize Terraform:**
   ```bash
   terraform init
   ```

2. **Plan the changes:**
   ```bash
   terraform plan
   ```

3. **Apply the configuration:**
   ```bash
   terraform apply
   ```

---

### Outputs

After deployment, Terraform provides the following outputs:

- **Lambda Function ARN:** The Amazon Resource Name (ARN) of the deployed Lambda function.
- **Lambda Layer ARN:** The ARN of the deployed Lambda Layer.

---

### Summary

This setup includes:
- A Lambda function (`TechJobBot`) with an associated IAM execution role.
- A Lambda Layer to manage Python dependencies.
- Outputs that include ARNs for both the Lambda function and Lambda Layer.

---

### Release History

- **Version 0.0.1:** Initial work in progress.

---

### Contributing

For contribution guidelines, review the [CONTRIBUTION.md](CONTRIBUTION.md) file.

---

### Python Packages Used

The following Python packages are included in the Lambda Layer:

- [Tweepy](https://docs.tweepy.org/en/stable/)
- [Gspread](https://docs.gspread.org/en/latest/)
- [OAuth2Client](https://oauth2client.readthedocs.io/)
- [Requests](https://docs.python-requests.org/en/master/)
- [SIB API v3 SDK](https://developers.sendinblue.com/reference/sib-api-v3-sdk-python)

---

### Local Environment Setup

Follow these steps to set up a local development environment:

1. **Move to Python directory:**
   ```bash
   cd lambda/part_time_pulse
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Check Installed Packages:**
   ```bash
   pip list --local
   ```

6. **Deactivate the Virtual Environment:**
   ```bash
   deactivate
   ```

---

### Running Locally

To run the project locally, ensure you have installed all the dependencies listed in the [requirements.txt](requirements.txt) file.

For additional help, refer to the links provided:
- [Virtual Env - venv](https://docs.python.org/3/library/venv.html)

---

This document serves as a comprehensive guide for deploying and managing an AWS Lambda function and Lambda Layer using Terraform, with detailed instructions for setting up and running a local Python development environment.