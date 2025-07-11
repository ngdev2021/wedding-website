#!/bin/bash

# Environment Switcher for Wedding Website
# This script helps switch between local and production image configurations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Wedding Website Environment Switcher${NC}"
echo "======================================"

# Check if config files exist
if [ ! -f "config.js" ]; then
    echo -e "${RED}❌ config.js not found!${NC}"
    exit 1
fi

if [ ! -f "config-production.js" ]; then
    echo -e "${RED}❌ config-production.js not found!${NC}"
    exit 1
fi

# Function to switch to local
switch_to_local() {
    echo -e "${BLUE}🔄 Switching to LOCAL environment...${NC}"
    
    # Check if we're already in local mode
    if grep -q "IMAGE_ENV = 'local'" config.js; then
        echo -e "${YELLOW}⚠️  Already in local mode${NC}"
        return
    fi
    
    # Backup current config
    cp config.js config.js.backup
    
    # Create local config
    cat > config.js << 'EOF'
// Image Configuration
// Set to 'local' for development, 'production' for GCP bucket
const IMAGE_ENV = 'local';

// GCP Configuration
const GCP_CONFIG = {
    bucketName: 'your-wedding-website-bucket', // Replace with your actual bucket name
    region: 'us-central1', // Replace with your preferred region
    projectId: 'your-project-id' // Replace with your GCP project ID
};

// Image paths configuration
const IMAGE_CONFIG = {
    local: {
        basePath: './images/',
        images: {
            proshot: 'proshot.jpg',
            party_red_black: 'party_red_black.jpg',
            champ_keke_red_black: 'champ-keke-red-black.jpg',
            cowboy_beige_white: 'cowboy_beige_white.jpg',
            jeep_life_red: 'jeep_life_red.jpg',
            marriage_license: 'marriage-license.jpg',
            vacation_swimsuit: 'vacation_swimsuit.jpg'
        }
    },
    production: {
        basePath: `https://storage.googleapis.com/${GCP_CONFIG.bucketName}/`,
        images: {
            proshot: 'proshot.jpg',
            party_red_black: 'party_red_black.jpg',
            champ_keke_red_black: 'champ-keke-red-black.jpg',
            cowboy_beige_white: 'cowboy_beige_white.jpg',
            jeep_life_red: 'jeep_life_red.jpg',
            marriage_license: 'marriage-license.jpg',
            vacation_swimsuit: 'vacation_swimsuit.jpg'
        }
    }
};

// Function to get image URL based on environment
function getImageUrl(imageKey) {
    const config = IMAGE_CONFIG[IMAGE_ENV];
    return config.basePath + config.images[imageKey];
}

// Function to get all image URLs
function getAllImageUrls() {
    const config = IMAGE_CONFIG[IMAGE_ENV];
    const urls = {};
    
    Object.keys(config.images).forEach(key => {
        urls[key] = config.basePath + config.images[key];
    });
    
    return urls;
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        IMAGE_ENV,
        GCP_CONFIG,
        IMAGE_CONFIG,
        getImageUrl,
        getAllImageUrls
    };
}
EOF

    echo -e "${GREEN}✅ Switched to LOCAL environment${NC}"
    echo -e "${YELLOW}📝 Images will now load from ./images/ directory${NC}"
}

# Function to switch to production
switch_to_production() {
    echo -e "${BLUE}🔄 Switching to PRODUCTION environment...${NC}"
    
    # Check if we're already in production mode
    if grep -q "IMAGE_ENV = 'production'" config.js; then
        echo -e "${YELLOW}⚠️  Already in production mode${NC}"
        return
    fi
    
    # Backup current config
    cp config.js config.js.backup
    
    # Copy production config
    cp config-production.js config.js
    
    echo -e "${GREEN}✅ Switched to PRODUCTION environment${NC}"
    echo -e "${YELLOW}📝 Images will now load from GCP bucket${NC}"
    echo -e "${YELLOW}⚠️  Remember to update bucket name and project ID in config.js${NC}"
}

# Function to show current status
show_status() {
    echo -e "${BLUE}📊 Current Environment Status:${NC}"
    
    if grep -q "IMAGE_ENV = 'local'" config.js; then
        echo -e "${GREEN}✅ Currently in LOCAL mode${NC}"
        echo -e "${YELLOW}📁 Images loading from: ./images/${NC}"
    elif grep -q "IMAGE_ENV = 'production'" config.js; then
        echo -e "${GREEN}✅ Currently in PRODUCTION mode${NC}"
        echo -e "${YELLOW}☁️  Images loading from: GCP bucket${NC}"
    else
        echo -e "${RED}❓ Unknown environment mode${NC}"
    fi
}

# Main menu
echo ""
echo -e "${YELLOW}Choose an option:${NC}"
echo "1) Switch to LOCAL (development)"
echo "2) Switch to PRODUCTION (GCP bucket)"
echo "3) Show current status"
echo "4) Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        switch_to_local
        ;;
    2)
        switch_to_production
        ;;
    3)
        show_status
        ;;
    4)
        echo -e "${BLUE}👋 Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Invalid choice. Please run the script again.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Environment switch completed!${NC}" 