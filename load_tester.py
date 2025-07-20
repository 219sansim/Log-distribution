import requests, time
from concurrent.futures import ThreadPoolExecutor

DISTRIBUTOR_URL = "http://localhost:6000/analyze"

def send_log():
    log = {"log": "test log"}
    try:
        resp = requests.post(DISTRIBUTOR_URL, json=log, timeout=5)
        return resp.status_code == 200
    except requests.exceptions.RequestException as e:
        return False

success = 0
total = 500
start = time.time()

with ThreadPoolExecutor(max_workers=50) as pool:
    results = list(pool.map(lambda _: send_log(), range(total)))

success = sum(results)
end = time.time()

print(f"Sent {total} logs in {end-start:.2f}s, Success: {success}, Throughput: {success / (end - start):.2f} logs/sec")
