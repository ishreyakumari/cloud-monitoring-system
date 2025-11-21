import base64
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime, timedelta
from google.cloud import firestore

db = firestore.Client()
last_email_time = {}

def process_log(event, context):
    """Process logs from Pub/Sub and send email alerts"""
    
    # Decode the Pub/Sub message
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    log_entry = json.loads(pubsub_message)
    
    # Extract log details
    severity = log_entry.get('severity', 'UNKNOWN')
    message = log_entry.get('textPayload', 'No message')
    timestamp = log_entry.get('timestamp', 'Unknown time')
    source = log_entry.get('resource', {}).get('type', 'unknown')
    
    print(f"[{severity}] {timestamp}: {message}")
    
    # Store log in Firestore
    try:
        log_doc = {
            'severity': severity,
            'message': message,
            'timestamp': timestamp,
            'source': source,
            'raw_entry': log_entry,
            'created_at': firestore.SERVER_TIMESTAMP
        }
        db.collection('logs').add(log_doc)
        print(f"✅ Log stored in Firestore")
    except Exception as e:
        print(f"❌ Failed to store log in Firestore: {e}")
    
    # Send email alert on errors
    if severity == 'ERROR':
        print(f"🚨 ALERT: Error detected - {message}")
        
        current_time = datetime.now()
        message_key = f"{severity}_{message}"
        
        if message_key not in last_email_time:
            send_email_alert(severity, message, timestamp)
            last_email_time[message_key] = current_time
        else:
            time_diff = current_time - last_email_time[message_key]
            if time_diff >= timedelta(minutes=30):
                send_email_alert(severity, message, timestamp)
                last_email_time[message_key] = current_time
            else:
                print(f"⏳ Email skipped - last sent {time_diff.seconds//60} minutes ago")
    
    return 'Log processed'

def send_email_alert(severity, message, timestamp):
    """Send email alert for errors"""
    
    # Email configuration (you'll need to set these)
    sender_email = os.environ.get('SENDER_EMAIL', 'your-email@gmail.com')
    receiver_email = os.environ.get('RECEIVER_EMAIL', 'alert-email@gmail.com')
    password = os.environ.get('EMAIL_PASSWORD', '')  # App password for Gmail
    
    # Create email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f'🚨 Cloud Logging Alert: {severity}'
    
    body = f"""
    Cloud Logging Alert
    
    Severity: {severity}
    Time: {timestamp}
    Message: {message}
    
    This is an automated alert from your Cloud Logging Monitoring System.
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Send email via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        print(f"✅ Email alert sent to {receiver_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")