from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
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

@app.route('/admin')
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

@app.route('/api/guestbook/<message_id>', methods=['PUT'])
def update_guestbook(message_id):
    """Update an existing guestbook message"""
    try:
        data = request.get_json()
        guestbook_data = load_data(GUESTBOOK_FILE)
        
        # Find and update the guestbook message
        for message in guestbook_data:
            if message['id'] == message_id:
                message.update({
                    'name': data.get('name', message['name']),
                    'relationship': data.get('relationship', message['relationship']),
                    'message': data.get('message', message['message']),
                    'timestamp': datetime.now().isoformat()
                })
                save_data(GUESTBOOK_FILE, guestbook_data)
                return jsonify({
                    'success': True,
                    'message': 'Guestbook message updated successfully'
                })
        
        return jsonify({'error': 'Guestbook message not found'}), 404
    except Exception as e:
        print(f"Error updating guestbook message: {e}")
        return jsonify({'error': 'Failed to update guestbook message'}), 500

@app.route('/api/guestbook/<message_id>', methods=['DELETE'])
def delete_guestbook(message_id):
    """Delete a guestbook message"""
    try:
        guestbook_data = load_data(GUESTBOOK_FILE)
        
        # Find and remove the guestbook message
        for i, message in enumerate(guestbook_data):
            if message['id'] == message_id:
                deleted_name = message['name']
                guestbook_data.pop(i)
                save_data(GUESTBOOK_FILE, guestbook_data)
                return jsonify({
                    'success': True,
                    'message': f'Guestbook message from {deleted_name} deleted successfully'
                })
        
        return jsonify({'error': 'Guestbook message not found'}), 404
    except Exception as e:
        print(f"Error deleting guestbook message: {e}")
        return jsonify({'error': 'Failed to delete guestbook message'}), 500

@app.route('/api/rsvp/stats', methods=['GET'])
def get_rsvp_stats():
    """Get RSVP statistics with enhanced metrics"""
    try:
        rsvp_data = load_data(RSVP_FILE)
        waitlist_data = load_data(WAITLIST_FILE)
        guestbook_data = load_data(GUESTBOOK_FILE)
        
        # Basic RSVP stats
        attending = len([r for r in rsvp_data if r.get('attendance') == 'attending'])
        declining = len([r for r in rsvp_data if r.get('attendance') == 'declining'])
        total = len(rsvp_data)
        
        # Calculate rates
        attending_rate = f"{(attending / total * 100):.1f}%" if total > 0 else "0%"
        declining_rate = f"{(declining / total * 100):.1f}%" if total > 0 else "0%"
        
        # Recent activity (last 24 hours)
        now = datetime.now()
        yesterday = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        last_24h_rsvps = len([r for r in rsvp_data 
                             if datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00')).replace(tzinfo=None) > yesterday])
        
        # Waitlist stats
        waitlist_today = len([w for w in waitlist_data 
                             if datetime.fromisoformat(w['timestamp'].replace('Z', '+00:00')).replace(tzinfo=None) > yesterday])
        
        # Guestbook stats
        guestbook_today = len([g for g in guestbook_data 
                              if datetime.fromisoformat(g['timestamp'].replace('Z', '+00:00')).replace(tzinfo=None) > yesterday])
        
        # This week stats
        week_ago = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        guestbook_week = len([g for g in guestbook_data 
                             if datetime.fromisoformat(g['timestamp'].replace('Z', '+00:00')).replace(tzinfo=None) > week_ago])
        
        # Song requests
        song_requests = len([r for r in rsvp_data if r.get('song', '').strip()])
        
        # Most active day
        day_counts = {}
        for r in rsvp_data:
            date = datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00')).strftime('%A')
            day_counts[date] = day_counts.get(date, 0) + 1
        
        most_active_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else 'N/A'
        
        # Average response time (simplified - using submission time as proxy)
        if rsvp_data:
            # Calculate average time between submissions (as a proxy for response time)
            timestamps = [datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00')) for r in rsvp_data]
            timestamps.sort()
            if len(timestamps) > 1:
                intervals = [(timestamps[i+1] - timestamps[i]).total_seconds() / 3600 for i in range(len(timestamps)-1)]
                avg_interval = sum(intervals) / len(intervals)
                avg_response_time = f"{avg_interval:.1f} hours"
            else:
                avg_response_time = "N/A"
        else:
            avg_response_time = "N/A"
        
        return jsonify({
            'success': True,
            'stats': {
                'total': total,
                'attending': attending,
                'declining': declining,
                'pending': total - attending - declining,
                'attendingRate': attending_rate,
                'decliningRate': declining_rate,
                'last24h': last_24h_rsvps,
                'waitlistToday': waitlist_today,
                'guestbookToday': guestbook_today,
                'guestbookWeek': guestbook_week,
                'songRequests': song_requests,
                'mostActiveDay': most_active_day,
                'avgResponseTime': avg_response_time
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

@app.route('/api/rsvp/<rsvp_id>', methods=['PUT'])
def update_rsvp(rsvp_id):
    """Update an existing RSVP"""
    try:
        data = request.get_json()
        rsvp_data = load_data(RSVP_FILE)
        
        # Find and update the RSVP
        for rsvp in rsvp_data:
            if rsvp['id'] == rsvp_id:
                rsvp.update({
                    'name': data.get('name', rsvp['name']),
                    'attendance': data.get('attendance', rsvp['attendance']),
                    'song': data.get('song', rsvp.get('song', '')),
                    'timestamp': datetime.now().isoformat()
                })
                save_data(RSVP_FILE, rsvp_data)
                return jsonify({
                    'success': True,
                    'message': 'RSVP updated successfully'
                })
        
        return jsonify({'error': 'RSVP not found'}), 404
    except Exception as e:
        print(f"Error updating RSVP: {e}")
        return jsonify({'error': 'Failed to update RSVP'}), 500

@app.route('/api/rsvp/<rsvp_id>', methods=['DELETE'])
def delete_rsvp(rsvp_id):
    """Delete an RSVP"""
    try:
        rsvp_data = load_data(RSVP_FILE)
        
        # Find and remove the RSVP
        for i, rsvp in enumerate(rsvp_data):
            if rsvp['id'] == rsvp_id:
                deleted_name = rsvp['name']
                rsvp_data.pop(i)
                save_data(RSVP_FILE, rsvp_data)
                return jsonify({
                    'success': True,
                    'message': f'RSVP for {deleted_name} deleted successfully'
                })
        
        return jsonify({'error': 'RSVP not found'}), 404
    except Exception as e:
        print(f"Error deleting RSVP: {e}")
        return jsonify({'error': 'Failed to delete RSVP'}), 500

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

@app.route('/api/waitlist/<waitlist_id>', methods=['PUT'])
def update_waitlist(waitlist_id):
    """Update an existing waitlist entry"""
    try:
        data = request.get_json()
        waitlist_data = load_data(WAITLIST_FILE)
        
        # Find and update the waitlist entry
        for entry in waitlist_data:
            if entry['id'] == waitlist_id:
                entry.update({
                    'name': data.get('name', entry['name']),
                    'song': data.get('song', entry.get('song', '')),
                    'timestamp': datetime.now().isoformat()
                })
                save_data(WAITLIST_FILE, waitlist_data)
                return jsonify({
                    'success': True,
                    'message': 'Waitlist entry updated successfully'
                })
        
        return jsonify({'error': 'Waitlist entry not found'}), 404
    except Exception as e:
        print(f"Error updating waitlist entry: {e}")
        return jsonify({'error': 'Failed to update waitlist entry'}), 500

@app.route('/api/waitlist/<waitlist_id>', methods=['DELETE'])
def delete_waitlist(waitlist_id):
    """Delete a waitlist entry"""
    try:
        waitlist_data = load_data(WAITLIST_FILE)
        
        # Find and remove the waitlist entry
        for i, entry in enumerate(waitlist_data):
            if entry['id'] == waitlist_id:
                deleted_name = entry['name']
                waitlist_data.pop(i)
                save_data(WAITLIST_FILE, waitlist_data)
                return jsonify({
                    'success': True,
                    'message': f'Waitlist entry for {deleted_name} deleted successfully'
                })
        
        return jsonify({'error': 'Waitlist entry not found'}), 404
    except Exception as e:
        print(f"Error deleting waitlist entry: {e}")
        return jsonify({'error': 'Failed to delete waitlist entry'}), 500

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

@app.route('/api/import/rsvp', methods=['POST'])
def import_rsvp_data():
    """Import RSVP data from CSV"""
    try:
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({'error': 'No data provided'}), 400
        
        imported_count = 0
        existing_rsvps = load_data(RSVP_FILE)
        existing_names = {rsvp['name'].lower() for rsvp in existing_rsvps}
        
        for row in data['data']:
            # Validate required fields
            if not row.get('name'):
                continue
                
            # Skip if name already exists
            if row['name'].lower() in existing_names:
                continue
            
            # Create RSVP entry
            rsvp_entry = {
                'id': datetime.now().strftime('%Y%m%d_%H%M%S_%f'),
                'name': row['name'],
                'attendance': row.get('attendance', 'not_specified'),
                'song': row.get('song', ''),
                'timestamp': datetime.now().isoformat(),
                'ip_address': 'imported',
                'imported': True
            }
            
            existing_rsvps.append(rsvp_entry)
            existing_names.add(row['name'].lower())
            imported_count += 1
        
        save_data(RSVP_FILE, existing_rsvps)
        
        return jsonify({
            'success': True,
            'imported': imported_count,
            'message': f'Successfully imported {imported_count} RSVP records'
        })
        
    except Exception as e:
        print(f"Error importing RSVP data: {e}")
        return jsonify({'error': 'Failed to import RSVP data'}), 500

@app.route('/api/import/guests', methods=['POST'])
def import_guest_data():
    """Import guest list data from CSV"""
    try:
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({'error': 'No data provided'}), 400
        
        imported_count = 0
        existing_guests = load_data(GUESTBOOK_FILE)
        existing_names = {guest['name'].lower() for guest in existing_guests}
        
        for row in data['data']:
            # Validate required fields
            if not row.get('name'):
                continue
                
            # Skip if name already exists
            if row['name'].lower() in existing_names:
                continue
            
            # Create guest entry (as a guestbook message)
            guest_entry = {
                'id': datetime.now().strftime('%Y%m%d_%H%M%S_%f'),
                'name': row['name'],
                'relationship': row.get('category', 'Other'),
                'message': f"Imported guest: {row.get('email', 'No email')} | {row.get('phone', 'No phone')}",
                'timestamp': datetime.now().isoformat(),
                'ip_address': 'imported',
                'imported': True,
                'email': row.get('email', ''),
                'phone': row.get('phone', '')
            }
            
            existing_guests.append(guest_entry)
            existing_names.add(row['name'].lower())
            imported_count += 1
        
        save_data(GUESTBOOK_FILE, existing_guests)
        
        return jsonify({
            'success': True,
            'imported': imported_count,
            'message': f'Successfully imported {imported_count} guest records'
        })
        
    except Exception as e:
        print(f"Error importing guest data: {e}")
        return jsonify({'error': 'Failed to import guest data'}), 500

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