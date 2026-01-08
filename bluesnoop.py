import asyncio
from bleak import BleakScanner

async def scan_nearby():
    devices = await BleakScanner.discover()
    for d in devices:
        # RSSI is available in d.details or d.rssi
        print(f"ID: {d.address}, RSSI: {d.rssi} dBm")

def start():
    asyncio.run(scan_nearby())

if __name__ == "__main__":
    start()
