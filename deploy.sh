#!/bin/bash

# Wedding Website Production Deployment Script

echo "🚀 Starting Wedding Website Production Deployment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env_example.txt .env
    echo "⚠️  Please edit .env file with your email credentials before running in production."
fi

# Create data directories if they don't exist
echo "📁 Setting up data storage..."
mkdir -p data
touch data/rsvp_data.json
touch data/guestbook_data.json

# Set proper permissions
chmod 644 data/*.json

echo "✅ Production setup complete!"
echo ""
echo "🎯 To run in production mode:"
echo "   gunicorn --bind 0.0.0.0:5000 wsgi:app"
echo ""
echo "🎯 To run in development mode:"
echo "   python3 app.py"
echo ""
echo "🌐 Access your website at:"
echo "   Main site: http://localhost:5000"
echo "   Admin dashboard: http://localhost:5000/admin.html"
echo ""
echo "📧 Don't forget to configure your .env file with email settings!" 