# Wedding Website - Image Management

This wedding website is set up to load images locally during development and from a Google Cloud Storage bucket in production.

## 🏗️ Project Structure

```
wedding-website/
├── images/                    # Local image files
│   ├── proshot.jpg
│   ├── party_red_black.jpg
│   ├── champ-keke-red-black.jpg
│   ├── cowboy_beige_white.jpg
│   ├── jeep_life_red.jpg
│   ├── marriage-license.jpg
│   └── vacation_swimsuit.jpg
├── index.html                 # Main website file
├── config.js                  # Local development configuration
├── config-production.js       # Production configuration
├── deploy-images.sh          # GCP deployment script
├── env.example               # Environment variables template
└── README.md                 # This file
```

## 🚀 Quick Start

### Local Development

1. **Start with local images** (already configured):
   ```bash
   # The website is already set up to use local images
   # Just open index.html in your browser
   open index.html
   ```

2. **Images are loaded from the `./images/` directory**

### Production Deployment

1. **Set up Google Cloud Storage**:
   ```bash
   # Install Google Cloud SDK if you haven't already
   # https://cloud.google.com/sdk/docs/install
   
   # Authenticate with Google Cloud
   gcloud auth login
   ```

2. **Configure your GCP settings**:
   ```bash
   # Copy the environment template
   cp env.example .env
   
   # Edit .env with your actual GCP project details
   nano .env
   ```

3. **Update the deployment script**:
   ```bash
   # Edit deploy-images.sh and update these variables:
   # - BUCKET_NAME
   # - PROJECT_ID
   # - REGION
   ```

4. **Deploy images to GCP**:
   ```bash
   # Make the script executable (already done)
   chmod +x deploy-images.sh
   
   # Run the deployment script
   ./deploy-images.sh
   ```

5. **Switch to production configuration**:
   ```bash
   # Replace config.js with config-production.js
   cp config-production.js config.js
   
   # Update the bucket name and project ID in config.js
   ```

## 📁 Configuration Files

### `config.js` (Development)
- Set `IMAGE_ENV = 'local'`
- Images load from `./images/` directory
- Used for local development

### `config-production.js` (Production)
- Set `IMAGE_ENV = 'production'`
- Images load from GCP bucket URLs
- Used for production deployment

### Environment Variables (`env.example`)
```bash
GCP_PROJECT_ID=your-project-id
GCP_BUCKET_NAME=your-wedding-website-bucket
GCP_REGION=us-central1
IMAGE_ENV=local
```

## 🔧 Deployment Script

The `deploy-images.sh` script:

1. **Checks prerequisites** (gcloud, gsutil)
2. **Creates GCP bucket** (if it doesn't exist)
3. **Uploads all images** from `./images/` directory
4. **Makes bucket publicly readable**
5. **Displays public URLs** for your images

### Running the Script
```bash
./deploy-images.sh
```

The script will:
- Ask if you want to create the bucket (if it doesn't exist)
- Ask if you want to upload images
- Show you the public URLs for your images

## 🌐 Image URLs

After deployment, your images will be available at:
```
https://storage.googleapis.com/YOUR_BUCKET_NAME/proshot.jpg
https://storage.googleapis.com/YOUR_BUCKET_NAME/party_red_black.jpg
https://storage.googleapis.com/YOUR_BUCKET_NAME/champ-keke-red-black.jpg
https://storage.googleapis.com/YOUR_BUCKET_NAME/cowboy_beige_white.jpg
https://storage.googleapis.com/YOUR_BUCKET_NAME/jeep_life_red.jpg
https://storage.googleapis.com/YOUR_BUCKET_NAME/marriage-license.jpg
https://storage.googleapis.com/YOUR_BUCKET_NAME/vacation_swimsuit.jpg
```

## 🔄 Switching Between Environments

### To Production:
```bash
# 1. Deploy images to GCP
./deploy-images.sh

# 2. Switch to production config
cp config-production.js config.js

# 3. Update bucket name and project ID in config.js
```

### To Development:
```bash
# 1. Switch back to local config
# (config.js is already set for local development)
```

## 💡 Tips

1. **Test locally first**: Always test your website locally before deploying
2. **Image optimization**: Consider optimizing your images for web (compress, resize)
3. **Backup**: Keep a backup of your original images
4. **CDN**: For better performance, consider using a CDN in front of your GCS bucket

## 🛠️ Troubleshooting

### Common Issues:

1. **Images not loading locally**:
   - Check that images exist in the `./images/` directory
   - Verify file names match exactly (case-sensitive)

2. **GCP deployment fails**:
   - Ensure you're authenticated: `gcloud auth login`
   - Check your project ID: `gcloud config get-value project`
   - Verify bucket name is unique globally

3. **Images not loading in production**:
   - Check bucket permissions (should be publicly readable)
   - Verify image URLs in browser developer tools
   - Ensure config.js is using production settings

## 📞 Support

If you encounter issues:
1. Check the browser console for errors
2. Verify your GCP configuration
3. Ensure all image files exist and are properly named 