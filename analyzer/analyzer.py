from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

ANALYZER_LATENCY = 0.4

class Analyzer:
    def __init__(self):
        self.cnt = 0

    def analyze(self, log):
        self.cnt += 1
        print(f"[{self.cnt}] analyzed log:", log)

analyzer = Analyzer()

def analyze_log_async(log):
    threading.Thread(target=analyzer.analyze, args=(log,)).start()

@app.route("/analyze", methods=["POST"])
def analyze_endpoint():
    data = request.get_json()
    if not data or 'log' not in data:
        return jsonify({"error": "Missing 'log' field"}), 400
    
    time.sleep(ANALYZER_LATENCY)

    analyze_log_async(data['log'])
    return jsonify({"status": "log received"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
