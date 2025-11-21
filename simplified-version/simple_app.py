"""
SIMPLE LOG GENERATOR
This program creates fake logs and sends them to Google Cloud.
Perfect for testing your monitoring system!
"""

# Import libraries (like tools we need)
import google.cloud.logging  # Tool to send logs to Google Cloud
import logging  # Python's built-in logging tool
import time  # To add delays
import random  # To pick random things

# Step 1: Connect to Google Cloud Logging
print("Connecting to Google Cloud...")
client = google.cloud.logging.Client()

# Step 2: Tell Python to send logs to Cloud
client.setup_logging()
print("Connected! Ready to send logs.")

# Step 3: Create a list of example logs
# Each log has two parts: (severity, message)
example_logs = [
    ("INFO", "User logged in successfully"),
    ("INFO", "File uploaded"),
    ("WARNING", "Memory usage is high"),
    ("WARNING", "Slow database query"),
    ("ERROR", "Failed to connect to database"),
    ("ERROR", "Payment processing failed")
]

# Step 4: Keep generating logs forever
print("\nStarting to generate logs...")
print("Press Ctrl+C to stop\n")

while True:  # Loop forever
    # Pick a random log from our list
    severity, message = random.choice(example_logs)
    
    # Send the log based on its severity
    if severity == "INFO":
        logging.info(message)  # Send INFO log
    elif severity == "WARNING":
        logging.warning(message)  # Send WARNING log
    elif severity == "ERROR":
        logging.error(message)  # Send ERROR log
    
    # Print to screen so you can see it
    print(f"[{severity}] {message}")
    
    # Wait 5 seconds before sending next log
    time.sleep(5)
