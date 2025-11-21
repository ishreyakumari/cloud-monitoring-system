# Generate sample logs
import google.cloud.logging
import logging
import time
import random

client = google.cloud.logging.Client()
client.setup_logging()

logs = [
    ("INFO", "User logged in"),
    ("WARNING", "High memory usage"),
    ("ERROR", "Database connection failed")
]

while True:
    severity, message = random.choice(logs)
    if severity == "INFO":
        logging.info(message)
    elif severity == "WARNING":
        logging.warning(message)
    else:
        logging.error(message)
    print(f"[{severity}] {message}")
    time.sleep(5)
