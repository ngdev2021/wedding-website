#!/bin/bash

# Wedding Website Image Deployment Script
# This script uploads images to Google Cloud Storage bucket

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BUCKET_NAME="wedding-website-2025-regdev-1752188684"  # Unique bucket name
PROJECT_ID="wedding-website-2025"              # GCP project ID
REGION="us-central1"                      # Preferred region
IMAGES_DIR="./images"

echo -e "${BLUE}🚀 Wedding Website Image Deployment${NC}"
echo "=================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud SDK (gcloud) is not installed.${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if gsutil is available
if ! command -v gsutil &> /dev/null; then
    echo -e "${RED}❌ gsutil is not available. Please install Google Cloud SDK.${NC}"
    exit 1
fi

# Check if images directory exists
if [ ! -d "$IMAGES_DIR" ]; then
    echo -e "${RED}❌ Images directory not found: $IMAGES_DIR${NC}"
    exit 1
fi

# Function to check if bucket exists
check_bucket() {
    if gsutil ls -b "gs://$BUCKET_NAME" &> /dev/null; then
        echo -e "${GREEN}✅ Bucket exists: gs://$BUCKET_NAME${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Bucket does not exist: gs://$BUCKET_NAME${NC}"
        return 1
    fi
}

# Function to create bucket
create_bucket() {
    echo -e "${BLUE}📦 Creating bucket: gs://$BUCKET_NAME${NC}"
    
    # Set the project
    gcloud config set project $PROJECT_ID
    
    # Create the bucket
    gsutil mb -l $REGION gs://$BUCKET_NAME
    
    # Make bucket publicly readable
    gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME
    
    echo -e "${GREEN}✅ Bucket created successfully!${NC}"
}

# Function to upload images
upload_images() {
    echo -e "${BLUE}📤 Uploading images to gs://$BUCKET_NAME${NC}"
    
    # Upload all images from the images directory
    gsutil -m cp "$IMAGES_DIR"/*.jpg gs://$BUCKET_NAME/
    
    echo -e "${GREEN}✅ Images uploaded successfully!${NC}"
}

# Function to list uploaded images
list_images() {
    echo -e "${BLUE}📋 Listing uploaded images:${NC}"
    gsutil ls gs://$BUCKET_NAME/*.jpg
}

# Function to get public URLs
get_public_urls() {
    echo -e "${BLUE}🔗 Public URLs for your images:${NC}"
    echo "=================================="
    
    for file in "$IMAGES_DIR"/*.jpg; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            echo "https://storage.googleapis.com/$BUCKET_NAME/$filename"
        fi
    done
}

# Main execution
echo -e "${YELLOW}🔧 Checking prerequisites...${NC}"

# Check if bucket exists, create if it doesn't
if ! check_bucket; then
    echo -e "${YELLOW}Do you want to create the bucket? (y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        create_bucket
    else
        echo -e "${RED}❌ Cannot proceed without bucket. Exiting.${NC}"
        exit 1
    fi
fi

# Upload images
echo -e "${YELLOW}Do you want to upload images? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    upload_images
    list_images
    echo ""
    get_public_urls
else
    echo -e "${YELLOW}⏭️  Skipping image upload.${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Deployment script completed!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Update config.js with your actual bucket name and project ID"
echo "2. Set IMAGE_ENV to 'production' in config.js for production deployment"
echo "3. Test your website with the new image URLs" 