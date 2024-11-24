#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
BUILD_DIR="lambda_layer/python"
LAYER_ZIP="lambda_layer.zip"

# Step 1: Create a clean build directory for the layer
echo "Creating build directory..."
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# Step 2: Set up a virtual environment for dependencies
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 3: Install dependencies into the build directory
echo "Installing dependencies into the build directory..."
pip install \
    tweepy \
    gspread \
    oauth2client \
    requests \
    sib_api_v3_sdk \
    -t $BUILD_DIR

# Step 4: Create the Lambda Layer ZIP package
echo "Creating the Lambda layer package..."
cd lambda_layer
zip -r ../$LAYER_ZIP .
cd ..

# Step 5: Clean up the virtual environment
echo "Cleaning up..."
deactivate
rm -rf venv

# Step 6: Report layer package size
echo "Layer package size:"
ls -lh $LAYER_ZIP

echo "Done! Your Lambda Layer package is ready in $LAYER_ZIP"
