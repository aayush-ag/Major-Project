import os
import json
import time
import asyncio
from bleak import BleakScanner

CONTEXT_DIR = "context"  # Your folder with .txt, .json etc.

def load_context_files():
    combined_context = ""
    for filename in os.listdir(CONTEXT_DIR):
        path = os.path.join(CONTEXT_DIR, filename)
        if filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                combined_context += f"\n\n--- {filename} ---\n"
                combined_context += f.read()
        elif filename.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                combined_context += f"\n\n--- {filename} ---\n"
                combined_context += json.dumps(data, indent=2)
    return combined_context

async def scan_ble_devices(scan_duration=5.0):
    devices = await BleakScanner.discover(scan_duration, return_adv=True)
    ble_data = []
    for device, adv_data in devices.values():
        name = device.name or adv_data.local_name or "Unknown"
        ble_data.append({
            "address": device.address,
            "name": name,
            "rssi": adv_data.rssi,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        })
    return ble_data

async def main():
    print("📁 Loading context files...")
    context = load_context_files()

    print("📡 Scanning for BLE devices...")
    ble_data = await scan_ble_devices()
    ble_summary = "\n".join([f"{dev['name']} ({dev['address']}) RSSI: {dev['rssi']} @ {dev['timestamp']}" for dev in ble_data])

    full_prompt = f"""
You are a class assistant AI.

Context:
{context}

Nearby Bluetooth devices:
{ble_summary}
You will use the bluetooth with maximum rssi to determine the nearest device and select it and lets say you will use and give all the details about that class.
Using this information, answer queries about what's happening around or in the current room.
"""

    print("✅ Prompt ready for Ollama:\n")
    print(full_prompt[:1500] + "\n...\n[TRUNCATED]" if len(full_prompt) > 1500 else full_prompt)

    # Optional: Call Ollama
    import ollama
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": full_prompt}])
    print("🧠 Response:", response['message']['content'])

asyncio.run(main())

#Nearest
#Neigbhours

#Have option on node to check other devices bluetooth

























