import google.cloud.logging
import logging
import time
import random

# Initialize Cloud Logging client
client = google.cloud.logging.Client()
client.setup_logging()

def generate_sample_logs():
    """Generate sample logs with different severity levels"""
    
    log_messages = [
        ("INFO", "Application started successfully"),
        ("INFO", "User logged in"),
        ("WARNING", "High memory usage detected"),
        ("ERROR", "Database connection failed"),
        ("ERROR", "Payment processing failed"),
        ("INFO", "Request processed successfully"),
    ]
    
    while True:
        severity, message = random.choice(log_messages)
        
        if severity == "INFO":
            logging.info(message)
        elif severity == "WARNING":
            logging.warning(message)
        elif severity == "ERROR":
            logging.error(message)
        
        print(f"[{severity}] {message}")
        time.sleep(5)  # Wait 5 seconds between logs

if __name__ == "__main__":
    print("Starting log generator...")
    generate_sample_logs()