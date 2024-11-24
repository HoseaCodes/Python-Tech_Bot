#!/bin/bash

# Define variables
ZIP_NAME="application.zip"
EXCLUDE_DIR="oos"

# Check if .gitignore exists
if [[ ! -f .gitignore ]]; then
  echo ".gitignore not found! Make sure it exists in the root directory."
  exit 1
fi

# Create a temporary exclude file
EXCLUDE_FILE=".exclude_list"

# Add directories/files from .gitignore to the exclude list
echo "Creating exclude list from .gitignore..."
cat .gitignore > $EXCLUDE_FILE

# Add the custom directory to the exclude list
echo "$EXCLUDE_DIR" >> $EXCLUDE_FILE

# Create the zip file while excluding the specified directories and files
echo "Creating the zip package $ZIP_NAME..."
zip -r $ZIP_NAME .
# zip -r $ZIP_NAME . -x@${EXCLUDE_FILE}

# Clean up the temporary exclude list
rm -f $EXCLUDE_FILE

# Output success message
echo "Zip package created: $ZIP_NAME"
