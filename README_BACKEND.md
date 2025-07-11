# Wedding Website Backend Setup

This backend system collects RSVP responses and guest book messages from your wedding website.

## Features

- **RSVP Collection**: Collects guest responses with attendance status and song requests
- **Guest Book**: Stores messages from guests with their relationship to the couple
- **Email Notifications**: Sends email alerts when new submissions are received
- **Data Export**: Admin dashboard to view and export collected data
- **JSON Storage**: Simple file-based storage (no database required)

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Email Notifications (Optional)

Create a `.env` file in the project root:

```bash
# Email Configuration (for notifications)
# For Gmail, you'll need to use an App Password, not your regular password
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
COUPLE_EMAIL=your-email@gmail.com
```

**Gmail App Password Setup:**
1. Go to your Google Account settings
2. Enable 2-factor authentication
3. Generate an App Password for "Mail"
4. Use this App Password in the `.env` file

### 3. Run the Backend Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 4. Access Points

- **Main Website**: `http://localhost:5000/`
- **Admin Dashboard**: `http://localhost:5000/admin.html`
- **Health Check**: `http://localhost:5000/api/health`

## API Endpoints

### RSVP Endpoints

- `POST /api/rsvp` - Submit RSVP response
- `GET /api/rsvp` - Get all RSVP data (admin)
- `GET /api/rsvp/stats` - Get RSVP statistics

### Guest Book Endpoints

- `POST /api/guestbook` - Submit guest book message
- `GET /api/guestbook` - Get guest book messages

### Data Structure

**RSVP Entry:**
```json
{
  "id": "20241215_143022",
  "name": "John Doe",
  "attendance": "attending",
  "song": "Dancing Queen",
  "timestamp": "2024-12-15T14:30:22.123456",
  "ip_address": "192.168.1.1"
}
```

**Guest Book Entry:**
```json
{
  "id": "20241215_143022",
  "name": "Jane Smith",
  "relationship": "Friend",
  "message": "Congratulations! So happy for you both!",
  "timestamp": "2024-12-15T14:30:22.123456",
  "date": "December 15, 2024",
  "ip_address": "192.168.1.1"
}
```

## Admin Dashboard

The admin dashboard (`/admin.html`) provides:

- **Statistics Overview**: Total RSVPs, attending, declining, pending
- **RSVP Management**: View all RSVP responses in a table format
- **Guest Book Management**: View all guest book messages
- **Data Export**: Download RSVP and guest book data as CSV files

## Data Storage

Data is stored in JSON files:
- `rsvp_data.json` - RSVP responses
- `guestbook_data.json` - Guest book messages

These files are automatically created when the server starts.

## Security Notes

- The backend includes basic validation for required fields
- IP addresses are logged for potential spam prevention
- Email notifications help you monitor submissions in real-time
- Consider adding rate limiting for production use

## Production Deployment

For production deployment:

1. **Use a production WSGI server** (Gunicorn, uWSGI)
2. **Add environment variables** for email configuration
3. **Set up proper logging**
4. **Consider using a database** instead of JSON files for larger scale
5. **Add rate limiting** to prevent spam
6. **Set up HTTPS** for secure data transmission

## Troubleshooting

**Email not sending:**
- Check your Gmail App Password is correct
- Ensure 2-factor authentication is enabled
- Verify the email addresses in `.env`

**Data not saving:**
- Check file permissions in the project directory
- Ensure the server has write access to create JSON files

**Frontend not connecting:**
- Verify the backend is running on the correct port
- Check CORS settings if accessing from a different domain 