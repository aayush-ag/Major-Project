import asyncio
import time
from bleak import BleakScanner

async def scan_ble_devices(scan_duration=5.0):
    devices = await BleakScanner.discover(scan_duration, return_adv=True)
    ble_data = []
    for device, adv_data in devices.values():
        name = device.name or adv_data.local_name or "Unknown"
        ble_data.append({
            "address": device.address,
            "name": name,
            "rssi": adv_data.rssi,
            "timestamp": time.time()
        })
    return ble_data

async def continuous_scan():
    while True:
        data = await scan_ble_devices()
        print("Scanned BLE Data:", data)
        # Send this context to your database (see Step 3)
        # For example: await db_client.insert_ble_data(context)
        await asyncio.sleep(10)  # adjust the sleep time to 10-15 seconds

if __name__ == "__main__":
    asyncio.run(continuous_scan())
