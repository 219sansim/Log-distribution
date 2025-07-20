import time
import random
from datetime import datetime
import requests

ANALYZER_URL = 'http://localhost:6000/analyze'

LOG_LEVELS = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']
SERVICES = ['auth', 'payment', 'inventory', 'analytics', 'api-gateway']
MESSAGES = [
    "User login successful",
    "Payment processed",
    "Item added to cart",
    "Data sync completed",
    "Rate limit exceeded",
    "Unauthorized access attempt"
]

def generate_log_line():
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    level = random.choice(LOG_LEVELS)
    service = random.choice(SERVICES)
    message = random.choice(MESSAGES)
    return f"{timestamp} | {level} | {service} | {message}"

def send_log_to_analyzer(log_line):
    try:
        response = requests.post(ANALYZER_URL, json={"log": log_line})
        if response.status_code != 200:
            print(f"Failed to send log: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending log: {e}")

if __name__ == "__main__":
    while True:
        log = generate_log_line()
        send_log_to_analyzer(log)
        time.sleep(1)  # simulate log frequency
