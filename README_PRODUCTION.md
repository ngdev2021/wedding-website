# Wedding Website - Production Deployment Guide

This guide will help you deploy your wedding website to production with both frontend and backend working together seamlessly.

## 🚀 Quick Start

### 1. Run the Deployment Script
```bash
chmod +x deploy.sh
./deploy.sh
```

### 2. Configure Email (Optional)
Edit the `.env` file with your Gmail credentials:
```bash
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
COUPLE_EMAIL=your-email@gmail.com
```

### 3. Start the Production Server
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

## 📁 Production Architecture

### **Single Server Setup**
- **Flask Backend**: Serves API endpoints and static files
- **Frontend**: Served directly by Flask (no separate server needed)
- **Data Storage**: JSON files in `data/` directory
- **Email Notifications**: Gmail SMTP integration

### **File Structure**
```
wedding-website/
├── app.py              # Flask backend application
├── wsgi.py             # WSGI entry point for production
├── index.html          # Main wedding website
├── admin.html          # Admin dashboard
├── images/             # Wedding photos
├── data/               # Data storage directory
│   ├── rsvp_data.json
│   └── guestbook_data.json
├── requirements.txt    # Python dependencies
├── deploy.sh          # Deployment script
└── .env               # Environment configuration
```

## 🌐 Access Points

### **Production URLs**
- **Main Website**: `http://your-domain.com/`
- **Admin Dashboard**: `http://your-domain.com/admin.html`
- **API Health Check**: `http://your-domain.com/api/health`

### **API Endpoints**
- `POST /api/rsvp` - Submit RSVP
- `GET /api/rsvp` - Get all RSVP data (admin)
- `GET /api/rsvp/stats` - Get RSVP statistics
- `POST /api/guestbook` - Submit guest book message
- `GET /api/guestbook` - Get guest book messages

## 🔧 Production Commands

### **Development Mode**
```bash
python3 app.py
```

### **Production Mode (Gunicorn)**
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

### **Production Mode with Workers**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

### **Production Mode with SSL (if using reverse proxy)**
```bash
gunicorn --bind 127.0.0.1:5000 --workers 4 wsgi:app
```

## 🛡️ Security Considerations

### **Environment Variables**
- Store sensitive data in `.env` file
- Never commit `.env` to version control
- Use strong passwords for email accounts

### **File Permissions**
```bash
chmod 644 data/*.json
chmod 755 data/
```

### **Rate Limiting (Optional)**
For additional security, consider adding rate limiting:
```bash
pip install flask-limiter
```

## 📧 Email Configuration

### **Gmail Setup**
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password for "Mail"
3. Use the App Password in your `.env` file

### **Email Notifications**
- RSVP submissions trigger email alerts
- Guest book messages trigger email alerts
- Emails include submission details and timestamps

## 📊 Data Management

### **Data Storage**
- RSVP data: `data/rsvp_data.json`
- Guest book data: `data/guestbook_data.json`
- Automatic backup recommended

### **Data Export**
- Admin dashboard provides CSV export
- Data can be downloaded for analysis
- JSON files can be backed up directly

### **Backup Strategy**
```bash
# Daily backup script example
cp data/rsvp_data.json backup/rsvp_$(date +%Y%m%d).json
cp data/guestbook_data.json backup/guestbook_$(date +%Y%m%d).json
```

## 🌍 Domain & Hosting

### **Domain Configuration**
- Point your domain to your server's IP address
- Configure DNS A record: `your-domain.com` → `your-server-ip`

### **SSL Certificate (Recommended)**
```bash
# Using Let's Encrypt with Certbot
sudo certbot --nginx -d your-domain.com
```

### **Nginx Reverse Proxy (Optional)**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔍 Monitoring & Logs

### **Application Logs**
```bash
# View Flask logs
tail -f /var/log/wedding-website.log

# View Gunicorn logs
tail -f /var/log/gunicorn.log
```

### **Health Monitoring**
- Health check endpoint: `/api/health`
- Monitor data file sizes
- Check email delivery status

## 🚨 Troubleshooting

### **Common Issues**

**Website not loading:**
- Check if Flask/Gunicorn is running
- Verify port 5000 is accessible
- Check firewall settings

**Forms not submitting:**
- Verify API endpoints are working
- Check browser console for errors
- Ensure data directory has write permissions

**Email not sending:**
- Verify Gmail credentials in `.env`
- Check 2-factor authentication is enabled
- Use App Password, not regular password

**Admin dashboard not loading:**
- Ensure `admin.html` file exists
- Check file permissions
- Verify route is properly configured

### **Debug Mode**
For troubleshooting, enable debug mode:
```bash
export FLASK_ENV=development
python3 app.py
```

## 📈 Scaling Considerations

### **High Traffic**
- Increase Gunicorn workers: `--workers 8`
- Use load balancer for multiple servers
- Consider database instead of JSON files

### **Data Growth**
- Implement data archiving
- Set up automated backups
- Monitor disk space usage

## 🎯 Performance Optimization

### **Static Files**
- Images are served directly by Flask
- Consider CDN for large image files
- Optimize image sizes

### **Caching**
- Browser caching for static assets
- Consider Redis for session storage
- Implement API response caching

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review application logs
3. Test endpoints individually
4. Verify configuration files

---

**Happy Wedding Planning! 💒** 