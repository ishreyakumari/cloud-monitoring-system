# Cloud Function - processes logs automatically
import base64
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from google.cloud import firestore

db = firestore.Client()

def process_log(event, context):
    # Decode log message
    data = base64.b64decode(event['data']).decode('utf-8')
    log = json.loads(data)
    
    # Extract data
    severity = log.get('severity', 'UNKNOWN')
    message = log.get('textPayload', 'No message')
    timestamp = log.get('timestamp', '')
    
    # Save to Firestore
    db.collection('logs').add({
        'severity': severity,
        'message': message,
        'timestamp': timestamp,
        'created_at': firestore.SERVER_TIMESTAMP
    })
    
    # Send email for errors
    if severity == 'ERROR':
        send_email(severity, message, timestamp)
    
    return 'Done'

def send_email(severity, message, timestamp):
    sender = os.environ.get('SENDER_EMAIL')
    receiver = os.environ.get('RECEIVER_EMAIL')
    password = os.environ.get('EMAIL_PASSWORD')
    
    email = MIMEMultipart()
    email['From'] = sender
    email['To'] = receiver
    email['Subject'] = f'Alert: {severity} Detected'
    
    body = f"Severity: {severity}\nTime: {timestamp}\nMessage: {message}"
    email.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(email)
