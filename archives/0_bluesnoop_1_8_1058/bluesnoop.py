import asyncio
from bleak import BleakScanner

async def scan_nearby():
    devices = await BleakScanner.discover()
    index = 0
    for d in devices:
        # RSSI is available in d.details or d.rssi
        # FIELDS
        # - address: str
        # - fields
        # - name
        print(f" - {index}: Device ",
              f"Address: {d.address},",
              f"Details: {d.details}",
              f"Name: {d.name}")
        index += 1

def start():
    asyncio.run(scan_nearby())

if __name__ == "__main__":
    start()
