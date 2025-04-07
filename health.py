import asyncio
import threading

from database import remove_stale_devices


def start_health_check():
    def loop():
        while True:
            remove_stale_devices(30)
            asyncio.run(asyncio.sleep(30))

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
