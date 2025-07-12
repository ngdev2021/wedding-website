from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Data storage files
DATA_DIR = 'data'
RSVP_FILE = os.path.join(DATA_DIR, 'rsvp_data.json')
WAITLIST_FILE = os.path.join(DATA_DIR, 'waitlist_data.json')
GUESTBOOK_FILE = os.path.join(DATA_DIR, 'guestbook_data.json')
SITE_CONFIG_FILE = os.path.join(DATA_DIR, 'site_config.json')

# Ensure data files exist
def ensure_data_files():
    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(RSVP_FILE):
        with open(RSVP_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(GUESTBOOK_FILE):
        with open(GUESTBOOK_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(WAITLIST_FILE):
        with open(WAITLIST_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(SITE_CONFIG_FILE):
        with open(SITE_CONFIG_FILE, 'w') as f:
            json.dump({
                'showHotelInfo': True,
                'hotelName': 'Hampton Inn & Suites Ft. Worth-Burleson',
                'hotelAddress': '13251 Jake Ct, Burleson, TX 76028',
                'bookingLink': 'https://www.google.com/travel/search?ts=CAESCAoCCAMKAggDGhwSGhIUCgcI6Q8QARgeEgcI6Q8QARgfGAEyAhAAKgcKBToDVVNE&qs=CAEyFENnc0l0ZGlRamViNWhLTHRBUkFCOApCCREL08P7HO_8ikIJEQKS7AAeOhwDQgkRy6OAidTYq_NaUQgBMk2qAUoQASoKIgZob3RlbHMoADIfEAEiG4_fMcyX83ZMB4u11pHZG8IJuZmkvlGPnVOVDTIZEAIiFWhvdGVscyBpbiBidXJsZXNvbiB0eA&utm_campaign=sharing&utm_medium=link_btn&utm_source=htls'
            }, f)

# Initialize data files when app starts
ensure_data_files()

# Load data from files
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save data to files
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Email configuration
def send_email_notification(subject, message, recipient_email=None):
    """Send email notification to the couple"""
    try:
        # Get email credentials from environment variables
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASSWORD')
        couple_email = os.getenv('COUPLE_EMAIL', sender_email)
        
        if not sender_email or not sender_password:
            print("Email credentials not configured. Skipping email notification.")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = couple_email
        msg['Subject'] = f"Wedding Website: {subject}"
        
        # Add body
        msg.attach(MIMEText(message, 'html'))
        
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, couple_email, text)
        server.quit()
        
        print(f"Email notification sent: {subject}")
        return True
        
    except Exception as e:
        print(f"Failed to send email notification: {e}")
        return False

@app.route('/')
def index():
    """Serve the main wedding website"""
    return send_from_directory('.', 'index.html')

@app.route('/admin.html')
def admin():
    """Serve the admin dashboard"""
    return send_from_directory('.', 'admin.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files (images, etc.)"""
    return send_from_directory('.', filename)

@app.route('/api/rsvp', methods=['POST'])
def submit_rsvp():
    """Handle RSVP form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create RSVP entry
        rsvp_entry = {
            'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'name': data['name'],
            'attendance': data.get('attendance', 'not_specified'),
            'song': data.get('song', ''),
            'timestamp': datetime.now().isoformat(),
            'ip_address': request.remote_addr
        }
        
        # Load existing data
        rsvp_data = load_data(RSVP_FILE)
        rsvp_data.append(rsvp_entry)
        save_data(RSVP_FILE, rsvp_data)
        
        # Send email notification
        subject = "New RSVP Submission"
        message = f"""
        <h2>New RSVP Submission</h2>
        <p><strong>Name:</strong> {rsvp_entry['name']}</p>
        <p><strong>Attendance:</strong> {rsvp_entry['attendance']}</p>
        <p><strong>Song Request:</strong> {rsvp_entry['song'] if rsvp_entry['song'] else 'None'}</p>
        <p><strong>Submitted:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        """
        send_email_notification(subject, message)
        
        # Determine response message
        if rsvp_entry['attendance'] == 'attending':
            response_message = f"Thank you, {rsvp_entry['name']}! We can't wait to celebrate with you!"
        elif rsvp_entry['attendance'] == 'declining':
            response_message = f"Thank you for letting us know, {rsvp_entry['name']}. We'll miss you but understand!"
        else:
            response_message = f"Thank you for your RSVP, {rsvp_entry['name']}! We'll be in touch soon."
        
        return jsonify({
            'success': True,
            'message': response_message,
            'rsvp_id': rsvp_entry['id']
        })
        
    except Exception as e:
        print(f"Error processing RSVP: {e}")
        return jsonify({'error': 'Failed to process RSVP submission'}), 500

@app.route('/api/guestbook', methods=['POST'])
def submit_guestbook():
    """Handle guest book form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'relationship', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create guest book entry
        guestbook_entry = {
            'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'name': data['name'],
            'relationship': data['relationship'],
            'message': data['message'],
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%B %d, %Y'),
            'ip_address': request.remote_addr
        }
        
        # Load existing data
        guestbook_data = load_data(GUESTBOOK_FILE)
        guestbook_data.append(guestbook_entry)
        save_data(GUESTBOOK_FILE, guestbook_data)
        
        # Send email notification
        subject = "New Guest Book Message"
        message = f"""
        <h2>New Guest Book Message</h2>
        <p><strong>From:</strong> {guestbook_entry['name']}</p>
        <p><strong>Relationship:</strong> {guestbook_entry['relationship']}</p>
        <p><strong>Message:</strong></p>
        <blockquote style="border-left: 3px solid #ccc; padding-left: 15px; margin: 10px 0;">
            {guestbook_entry['message']}
        </blockquote>
        <p><strong>Submitted:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        """
        send_email_notification(subject, message)
        
        return jsonify({
            'success': True,
            'message': f"Thank you for your message, {guestbook_entry['name']}! We love reading your well wishes.",
            'entry_id': guestbook_entry['id']
        })
        
    except Exception as e:
        print(f"Error processing guest book entry: {e}")
        return jsonify({'error': 'Failed to process guest book submission'}), 500

@app.route('/api/guestbook', methods=['GET'])
def get_guestbook():
    """Retrieve guest book messages"""
    try:
        guestbook_data = load_data(GUESTBOOK_FILE)
        # Return only the last 20 messages to prevent overwhelming the frontend
        return jsonify({
            'success': True,
            'messages': guestbook_data[-20:]
        })
    except Exception as e:
        print(f"Error retrieving guest book data: {e}")
        return jsonify({'error': 'Failed to retrieve guest book data'}), 500

@app.route('/api/rsvp/stats', methods=['GET'])
def get_rsvp_stats():
    """Get RSVP statistics"""
    try:
        rsvp_data = load_data(RSVP_FILE)
        
        attending = len([r for r in rsvp_data if r.get('attendance') == 'attending'])
        declining = len([r for r in rsvp_data if r.get('attendance') == 'declining'])
        total = len(rsvp_data)
        
        return jsonify({
            'success': True,
            'stats': {
                'total': total,
                'attending': attending,
                'declining': declining,
                'pending': total - attending - declining
            }
        })
    except Exception as e:
        print(f"Error retrieving RSVP stats: {e}")
        return jsonify({'error': 'Failed to retrieve RSVP statistics'}), 500

@app.route('/api/rsvp', methods=['GET'])
def get_rsvp_data():
    """Retrieve all RSVP data"""
    try:
        rsvp_data = load_data(RSVP_FILE)
        return jsonify({
            'success': True,
            'rsvps': rsvp_data
        })
    except Exception as e:
        print(f"Error retrieving RSVP data: {e}")
        return jsonify({'error': 'Failed to retrieve RSVP data'}), 500

@app.route('/api/waitlist', methods=['POST'])
def submit_waitlist():
    """Handle waitlist form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create waitlist entry
        waitlist_entry = {
            'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'name': data['name'],
            'attendance': data.get('attendance', 'waitlist'),
            'song': data.get('song', ''),
            'timestamp': datetime.now().isoformat(),
            'ip_address': request.remote_addr
        }
        
        # Load existing data
        waitlist_data = load_data(WAITLIST_FILE)
        waitlist_data.append(waitlist_entry)
        save_data(WAITLIST_FILE, waitlist_data)
        
        # Send email notification
        subject = "New Waitlist Submission"
        message = f"""
        <h2>New Waitlist Submission</h2>
        <p><strong>Name:</strong> {waitlist_entry['name']}</p>
        <p><strong>Status:</strong> Waitlist</p>
        <p><strong>Song Request:</strong> {waitlist_entry['song'] if waitlist_entry['song'] else 'None'}</p>
        <p><strong>Submitted:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        """
        send_email_notification(subject, message)
        
        return jsonify({
            'success': True,
            'message': f"Thank you, {waitlist_entry['name']}! We've added you to our waitlist and will contact you if space becomes available.",
            'waitlist_id': waitlist_entry['id']
        })
        
    except Exception as e:
        print(f"Error processing waitlist entry: {e}")
        return jsonify({'error': 'Failed to process waitlist submission'}), 500

@app.route('/api/waitlist', methods=['GET'])
def get_waitlist_data():
    """Retrieve all waitlist data"""
    try:
        waitlist_data = load_data(WAITLIST_FILE)
        return jsonify({
            'success': True,
            'waitlist': waitlist_data
        })
    except Exception as e:
        print(f"Error retrieving waitlist data: {e}")
        return jsonify({'error': 'Failed to retrieve waitlist data'}), 500

@app.route('/api/site-config', methods=['GET'])
def get_site_config():
    """Retrieve site configuration"""
    try:
        config = load_data(SITE_CONFIG_FILE)
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        print(f"Error retrieving site config: {e}")
        return jsonify({'error': 'Failed to retrieve site configuration'}), 500

@app.route('/api/site-config', methods=['POST'])
def update_site_config():
    """Update site configuration"""
    try:
        data = request.get_json()
        config = load_data(SITE_CONFIG_FILE)
        
        # Update specific fields if provided, otherwise keep existing
        if 'showHotelInfo' in data:
            config['showHotelInfo'] = data['showHotelInfo']
        if 'hotelName' in data:
            config['hotelName'] = data['hotelName']
        if 'hotelAddress' in data:
            config['hotelAddress'] = data['hotelAddress']
        if 'bookingLink' in data:
            config['bookingLink'] = data['bookingLink']
        
        save_data(SITE_CONFIG_FILE, config)
        
        return jsonify({
            'success': True,
            'message': 'Site configuration updated successfully',
            'config': config
        })
    except Exception as e:
        print(f"Error updating site config: {e}")
        return jsonify({'error': 'Failed to update site configuration'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'data_files': {
            'rsvp': os.path.exists(RSVP_FILE),
            'waitlist': os.path.exists(WAITLIST_FILE),
            'guestbook': os.path.exists(GUESTBOOK_FILE),
            'site_config': os.path.exists(SITE_CONFIG_FILE)
        }
    })

if __name__ == '__main__':
    ensure_data_files()
    print("Wedding website backend started!")
    print("Data files initialized:", RSVP_FILE, "and", GUESTBOOK_FILE)
    app.run(debug=True, host='0.0.0.0', port=5000) 