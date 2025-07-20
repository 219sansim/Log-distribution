from flask import Flask, request, jsonify
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import socket

app = Flask(__name__)

#Distribution weights
DISTRIBUTION_WEIGHTS = [1,1,1]

#WORKERS
WORKERS = 50

# Define backends with weights
BACKEND_CONFIG = []

executor = ThreadPoolExecutor(max_workers=WORKERS)

def initialize_analyzers():
    try:
        ips = socket.gethostbyname_ex("analyzer")[2]
        for i in range(len(ips)):
            ip = ips[i]
            BACKEND_CONFIG.append({"url": "http://"+ip+":5000/analyze", "health_url": "http://"+ip+":5000/health", "weight": DISTRIBUTION_WEIGHTS[i]})
        return [f"http://{ip}:6000/analyze" for ip in ips]
    except Exception as e:
        print("Error resolving analyzer service:", e)
        return []


# Flattened list based on weights for simple WRR
WEIGHTED_BACKEND_RING = []
for backend in BACKEND_CONFIG:
    WEIGHTED_BACKEND_RING.extend([backend["url"]] * backend["weight"])

lock = threading.Lock()
wrr_index = 0


def update_healthy_backends():
    global WEIGHTED_BACKEND_RING
    while True:
        current_healthy = []
        for backend in BACKEND_CONFIG:
            try:
                resp = requests.get(backend["health_url"], timeout=0.5)
                if resp.status_code == 200:
                    current_healthy.extend([backend["url"]] * backend["weight"])
            except requests.RequestException:
                pass  # Unhealthy
        with lock:
            WEIGHTED_BACKEND_RING = current_healthy
        time.sleep(0.1)  # check every 0.1 seconds

def get_next_backend():
    global wrr_index
    with lock:
        backend = WEIGHTED_BACKEND_RING[wrr_index]
        wrr_index = (wrr_index + 1) % len(WEIGHTED_BACKEND_RING)
    return backend

@app.route('/analyze', methods=['POST'])
def analyze_route():
    data = request.get_json()
    if not data or 'log' not in data:
        return jsonify({"error": "Missing 'log' field"}), 400

    backend_url = get_next_backend()

    def forward():
        return requests.post(backend_url, json=data, timeout=1)

    future = executor.submit(forward)
    try:
        resp = future.result(timeout=1.5)
        return jsonify({"forwarded_to": backend_url, "status": "ok"}), resp.status_code
    except Exception as e:
        return jsonify({"error": f"Failed to forward to backend: {e}"}), 502

if __name__ == '__main__':
    initialize_analyzers()
    threading.Thread(target=update_healthy_backends, daemon=True).start()
    app.run(host="0.0.0.0", port=6000, threaded=True)
