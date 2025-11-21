"""
SIMPLE CLOUD FUNCTION
This runs automatically when a log arrives.
It stores the log in Firestore and sends email alerts.
"""

import base64
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime, timedelta
from google.cloud import firestore

# Connect to Firestore database
db = firestore.Client()

# Remember when we last sent an email (to avoid spam)
last_email_time = {}


def process_log(event, context):
    """
    This function runs when a log arrives from Pub/Sub
    
    Steps:
    1. Decode the log message
    2. Extract important information
    3. Store in Firestore
    4. Send email if it's an error
    """
    
    # Step 1: Decode the message from Pub/Sub
    # (Pub/Sub sends messages in encoded format)
    encoded_data = event['data']
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    log_entry = json.loads(decoded_data)
    
    # Step 2: Extract information from the log
    severity = log_entry.get('severity', 'UNKNOWN')
    message = log_entry.get('textPayload', 'No message')
    timestamp = log_entry.get('timestamp', 'Unknown time')
    source = log_entry.get('resource', {}).get('type', 'unknown')
    
    print(f"Received: [{severity}] {message}")
    
    # Step 3: Store in Firestore database
    try:
        log_document = {
            'severity': severity,
            'message': message,
            'timestamp': timestamp,
            'source': source,
            'created_at': firestore.SERVER_TIMESTAMP
        }
        db.collection('logs').add(log_document)
        print("✅ Saved to database")
    except Exception as e:
        print(f"❌ Failed to save: {e}")
    
    # Step 4: Send email alert for errors
    if severity == 'ERROR':
        print("🚨 Error detected! Checking if we should send email...")
        
        current_time = datetime.now()
        message_key = f"{severity}_{message}"
        
        # Check when we last sent an email for this error
        if message_key not in last_email_time:
            # First time seeing this error, send email
            send_email_alert(severity, message, timestamp)
            last_email_time[message_key] = current_time
        else:
            # We've seen this error before
            time_since_last_email = current_time - last_email_time[message_key]
            minutes_passed = time_since_last_email.seconds // 60
            
            if time_since_last_email >= timedelta(minutes=30):
                # More than 30 minutes passed, send email
                send_email_alert(severity, message, timestamp)
                last_email_time[message_key] = current_time
            else:
                print(f"⏳ Skipping email (last sent {minutes_passed} minutes ago)")
    
    return 'Log processed successfully'


def send_email_alert(severity, message, timestamp):
    """
    Send an email alert
    
    This uses Gmail's SMTP server to send emails.
    You need an "App Password" from Google to use this.
    """
    
    # Get email settings from environment variables
    sender_email = os.environ.get('SENDER_EMAIL')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    password = os.environ.get('EMAIL_PASSWORD')
    
    # Create the email
    email = MIMEMultipart()
    email['From'] = sender_email
    email['To'] = receiver_email
    email['Subject'] = f'🚨 Alert: {severity} Log Detected'
    
    # Email body
    body = f"""
    Cloud Log Monitoring Alert
    ===========================
    
    Severity: {severity}
    Time: {timestamp}
    Message: {message}
    
    This is an automated alert from your monitoring system.
    """
    
    email.attach(MIMEText(body, 'plain'))
    
    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start secure connection
            server.login(sender_email, password)
            server.send_message(email)
        print(f"✅ Email sent to {receiver_email}")
    except Exception as e:
        print(f"❌ Email failed: {e}")
