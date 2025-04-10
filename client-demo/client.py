import asyncio
import httpx
import toml

CONFIG = toml.load("config.toml")
SERVER_URL = CONFIG["server"]["url"]
TOKEN = CONFIG["server"]["token"]
NODE_ID = CONFIG["server"]["id"]
LOCATION = CONFIG["server"]["location"]

known_addresses = set()

# 🔄 Dummy list of nearby addresses (replace this with dynamic input later if needed)
def get_current_addresses():
    return {
        "6C:F6:DA:80:1B:68",
        "AA:BB:CC:DD:EE:02",
        "AA:BB:CC:DD:EE:03",
        "AA:BB:CC:DD:EE:04",
        "6C:F6:DA:80:1B:69",
        "AA:BB:CC:DD:EE:05",  # <- Example devices seen around
    }

async def send_node_info():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {TOKEN}"}
                payload = {"id": NODE_ID, "location": LOCATION}
                response = await client.post(f"{SERVER_URL}/nodes/insert", headers=headers, json=payload)
                response.raise_for_status()
                print(f"[INFO] Node info sent: {payload}")
        except Exception as e:
            print(f"[ERROR] Failed to send node info: {e}")
        await asyncio.sleep(30)

async def update_known_addresses():
    global known_addresses
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {TOKEN}"}
            response = await client.get(f"{SERVER_URL}/nodes/", headers=headers)
            response.raise_for_status()
            data = response.json()
            known_addresses = {node["address"] for node in data if "address" in node}
            print(f"[INFO] Known addresses updated: {len(known_addresses)} entries")
    except Exception as e:
        print(f"[ERROR] Failed to update known addresses: {e}")

async def send_neighbour_count(count: int):
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {TOKEN}"}
            payload = {"node_id": NODE_ID, "neighbours": count}
            response = await client.post(f"{SERVER_URL}/neighbours/insert", headers=headers, json=payload)
            response.raise_for_status()
            print(f"[INFO] Sent neighbour count: {payload}")
    except Exception as e:
        print(f"[ERROR] Failed to send neighbour count: {e}")

async def continuous_scan():
    while True:
        await update_known_addresses()
        current_addresses = get_current_addresses()
        filtered_count = len(current_addresses - known_addresses)
        print(f"[BLE] Detected {filtered_count} new devices (excluding known addresses)")
        await send_neighbour_count(filtered_count)
        await asyncio.sleep(10)

async def main():
    await asyncio.gather(
        send_node_info(),
        continuous_scan()
    )

if __name__ == "__main__":
    asyncio.run(main())
