// Production Image Configuration for GCP Bucket
// This file should be used when deploying to production

const IMAGE_ENV = 'production';

// GCP Configuration - UPDATE THESE WITH YOUR ACTUAL VALUES
const GCP_CONFIG = {
    bucketName: 'wedding-website-2025-regdev-1752188684', // Unique bucket name
    region: 'us-central1', // Preferred region
    projectId: 'wedding-website-2025' // GCP project ID
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