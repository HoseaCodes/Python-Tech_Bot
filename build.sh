#!/bin/bash

# Create a clean build directory
echo "Creating build directory..."
BUILD_DIR="lambda_build"
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# Create and activate virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies into the build directory
echo "Installing dependencies..."
pip install \
    tweepy \
    gspread \
    oauth2client \
    requests \
    -t $BUILD_DIR

# Copy your Lambda function code
echo "Copying Lambda function code..."
cp *.py $BUILD_DIR/

# Create deployment package
echo "Creating deployment package..."
cd $BUILD_DIR
zip -r ../function.zip .
cd ..

# Clean up
echo "Cleaning up..."
deactivate
rm -rf venv

# Report package size
echo "Deployment package size:"
ls -lh function.zip

echo "Done! Your deployment package is ready in function.zip"
