import requests
import random
import time

SERVER_URL = "http://localhost:8000/ingest"

def send_random_device():
    for i in range(5):
        uid = f"device_{i}"
        rssi = random.randint(-90, -30)
        res = requests.post(SERVER_URL, json={"uid": uid, "rssi": rssi})
        print(res.json())

if __name__ == "__main__":
    while True:
        send_random_device()
        time.sleep(10)