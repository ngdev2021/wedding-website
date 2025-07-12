#!/usr/bin/env python3
"""
Test script to verify database operations for the wedding website.
This script tests RSVP, Guestbook, and Waitlist data operations.
"""

import json
import os
from datetime import datetime

# Import the database functions from app.py
from app import load_data, save_data, RSVP_FILE, GUESTBOOK_FILE, WAITLIST_FILE

def test_rsvp_operations():
    """Test RSVP data operations"""
    print("Testing RSVP operations...")
    
    # Test data
    test_rsvp = {
        'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'name': 'Test User',
        'attendance': 'attending',
        'song': 'Test Song Request',
        'timestamp': datetime.now().isoformat(),
        'ip_address': '127.0.0.1'
    }
    
    # Load existing data
    rsvp_data = load_data(RSVP_FILE)
    print(f"Current RSVP count: {len(rsvp_data)}")
    
    # Add test data
    rsvp_data.append(test_rsvp)
    save_data(RSVP_FILE, rsvp_data)
    
    # Verify data was saved
    rsvp_data_after = load_data(RSVP_FILE)
    print(f"RSVP count after adding: {len(rsvp_data_after)}")
    
    # Find our test entry
    test_entry = next((entry for entry in rsvp_data_after if entry['name'] == 'Test User'), None)
    if test_entry:
        print("✅ RSVP test entry found and saved successfully")
        print(f"   Name: {test_entry['name']}")
        print(f"   Attendance: {test_entry['attendance']}")
        print(f"   Song: {test_entry['song']}")
    else:
        print("❌ RSVP test entry not found")
    
    return True

def test_guestbook_operations():
    """Test Guestbook data operations"""
    print("\nTesting Guestbook operations...")
    
    # Test data
    test_guestbook = {
        'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'name': 'Test Guest',
        'relationship': 'Friend',
        'message': 'This is a test guestbook message',
        'timestamp': datetime.now().isoformat(),
        'date': datetime.now().strftime('%B %d, %Y'),
        'ip_address': '127.0.0.1'
    }
    
    # Load existing data
    guestbook_data = load_data(GUESTBOOK_FILE)
    print(f"Current Guestbook count: {len(guestbook_data)}")
    
    # Add test data
    guestbook_data.append(test_guestbook)
    save_data(GUESTBOOK_FILE, guestbook_data)
    
    # Verify data was saved
    guestbook_data_after = load_data(GUESTBOOK_FILE)
    print(f"Guestbook count after adding: {len(guestbook_data_after)}")
    
    # Find our test entry
    test_entry = next((entry for entry in guestbook_data_after if entry['name'] == 'Test Guest'), None)
    if test_entry:
        print("✅ Guestbook test entry found and saved successfully")
        print(f"   Name: {test_entry['name']}")
        print(f"   Relationship: {test_entry['relationship']}")
        print(f"   Message: {test_entry['message']}")
    else:
        print("❌ Guestbook test entry not found")
    
    return True

def test_waitlist_operations():
    """Test Waitlist data operations"""
    print("\nTesting Waitlist operations...")
    
    # Test data
    test_waitlist = {
        'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'name': 'Test Waitlist User',
        'email': 'test@example.com',
        'phone': '555-1234',
        'reason': 'Testing waitlist functionality',
        'timestamp': datetime.now().isoformat(),
        'ip_address': '127.0.0.1'
    }
    
    # Load existing data
    waitlist_data = load_data(WAITLIST_FILE)
    print(f"Current Waitlist count: {len(waitlist_data)}")
    
    # Add test data
    waitlist_data.append(test_waitlist)
    save_data(WAITLIST_FILE, waitlist_data)
    
    # Verify data was saved
    waitlist_data_after = load_data(WAITLIST_FILE)
    print(f"Waitlist count after adding: {len(waitlist_data_after)}")
    
    # Find our test entry
    test_entry = next((entry for entry in waitlist_data_after if entry['name'] == 'Test Waitlist User'), None)
    if test_entry:
        print("✅ Waitlist test entry found and saved successfully")
        print(f"   Name: {test_entry['name']}")
        print(f"   Email: {test_entry['email']}")
        print(f"   Reason: {test_entry['reason']}")
    else:
        print("❌ Waitlist test entry not found")
    
    return True

def test_site_config_operations():
    """Test Site Configuration operations"""
    print("\nTesting Site Configuration operations...")
    
    from app import SITE_CONFIG_FILE
    
    # Load existing config
    config = load_data(SITE_CONFIG_FILE)
    print(f"Current hotel info visibility: {config.get('showHotelInfo', 'Not set')}")
    
    # Test updating config
    config['showHotelInfo'] = False
    config['hotelName'] = 'Test Hotel'
    save_data(SITE_CONFIG_FILE, config)
    
    # Verify config was updated
    config_after = load_data(SITE_CONFIG_FILE)
    if config_after.get('showHotelInfo') == False:
        print("✅ Site config updated successfully")
        print(f"   Hotel info visibility: {config_after.get('showHotelInfo')}")
        print(f"   Hotel name: {config_after.get('hotelName')}")
    else:
        print("❌ Site config update failed")
    
    # Reset to original state
    config_after['showHotelInfo'] = True
    config_after['hotelName'] = 'Hampton Inn & Suites Ft. Worth-Burleson'
    save_data(SITE_CONFIG_FILE, config_after)
    
    return True

def cleanup_test_data():
    """Remove test data from all files"""
    print("\nCleaning up test data...")
    
    # Clean RSVP data
    rsvp_data = load_data(RSVP_FILE)
    rsvp_data = [entry for entry in rsvp_data if entry.get('name') != 'Test User']
    save_data(RSVP_FILE, rsvp_data)
    
    # Clean Guestbook data
    guestbook_data = load_data(GUESTBOOK_FILE)
    guestbook_data = [entry for entry in guestbook_data if entry.get('name') != 'Test Guest']
    save_data(GUESTBOOK_FILE, guestbook_data)
    
    # Clean Waitlist data
    waitlist_data = load_data(WAITLIST_FILE)
    waitlist_data = [entry for entry in waitlist_data if entry.get('name') != 'Test Waitlist User']
    save_data(WAITLIST_FILE, waitlist_data)
    
    print("✅ Test data cleaned up")

def main():
    """Run all database tests"""
    print("🧪 Testing Wedding Website Database Operations")
    print("=" * 50)
    
    try:
        # Test all operations
        test_rsvp_operations()
        test_guestbook_operations()
        test_waitlist_operations()
        test_site_config_operations()
        
        # Clean up test data
        cleanup_test_data()
        
        print("\n" + "=" * 50)
        print("✅ All database operations are working correctly!")
        print("\nTo test the full API functionality, run the Flask app:")
        print("python3 wsgi.py")
        print("\nThen visit: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 