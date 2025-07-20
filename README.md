# 🧪 Log Distributor System

This project simulates a high-throughput log distribution system where logs are routed to multiple analyzers based on a specified weight distribution. You can test system performance using the built-in load tester and tune key parameters for experimentation.

---

## 🚀 Getting Started

### 1. Run the Log Distributor

Spin up the system with a specified number of log analyzers:

```bash
docker-compose up --build --scale analyzer=3
```

## ⚙️ Configure Weight Distribution

Specify how logs should be routed to different analyzers by modifying the `DISTRIBUTION_WEIGHTS` list in [`distributor.py`](./distributor/distributor.py):

```python
DISTRIBUTION_WEIGHTS = [1, 1, 1]
```
## 🧪 Load Testing

To simulate incoming log traffic and evaluate system performance, use the built-in load tester.

```python
python3 load_tester.py
```

## 🧪 Simulate Failure Testing

To simulate analyzer failures, stop one of the analyzer containers. The load will be redistributed according to the weights- example `{analyzer-1: 1, analyzer-2: 2, analyzer-3: 3}`, we kill analyzer-1, the load distribution will be `{analyzer-2: 2, anlayzer-3: 3}`


```
docker stop {container-id-analyzer}
```

### Prerequisites

Ensure the `requests` library is installed:

```bash
pip install requests
```

## ⚙️ Tunables

You can adjust the following parameters to observe system behavior under different conditions:

### 🔧 Analyzer Latency

Simulate log processing time in [`analyzer.py`](./analyzer/analyzer.py) by modifying:

```
ANALYZER_LATENCY = 0.5  # seconds
```

### 🔧 Distributor worker threads

Control number of worker threads [`distributor.py`](./distributor/distributor.py) by modifying:

```
WORKERS=10
```
