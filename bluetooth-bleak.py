"""
Improved BLE Scanner
--------------------

Scans for BLE devices and shows extended information:
- Device name (fallback)
- RSSI
- Manufacturer data
- Service UUIDs
- Service data

Compatible with Windows/Linux/macOS (w/ bleak)

Updated by ChatGPT on 2025-04-05
"""

import argparse
import asyncio
from bleak import BleakScanner

async def main(args: argparse.Namespace):
    print("🔍 Scanning for BLE devices for 5 seconds...\n")

    devices = await BleakScanner.discover(
        return_adv=True,
        service_uuids=args.services,
        cb=dict(use_bdaddr=args.macos_use_bdaddr),
    )

    if not devices:
        print("❌ No devices found.")
        return

    for d, a in devices.values():
        name = d.name or a.local_name or "❓ Unknown"

        print(f"📡 Address: {d.address}")
        print(f"🔠 Name   : {name}")
        print(f"📶 RSSI   : {a.rssi} dBm")

        if a.manufacturer_data:
            print("🏷️  Manufacturer Data:")
            for k, v in a.manufacturer_data.items():
                print(f"   - ID {k}: {v.hex()}")

        if a.service_uuids:
            print("🔗 Service UUIDs:")
            for uuid in a.service_uuids:
                print(f"   - {uuid}")

        if a.service_data:
            print("📦 Service Data:")
            for k, v in a.service_data.items():
                print(f"   - {k}: {v.hex()}")

        print("-" * 40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--services", metavar="<uuid>", nargs="*", help="Filter by service UUIDs")
    parser.add_argument("--macos-use-bdaddr", action="store_true", help="Use Bluetooth address on macOS")
    args = parser.parse_args()

    asyncio.run(main(args))
