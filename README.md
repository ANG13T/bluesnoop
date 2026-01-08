# bluesnoop
A simple Bluetooth Low Energy (BLE) sniffer using Python and the Bleak library

#### Grant Bluetooth Permissions
Since you are using iTerm2, you need to ensure the terminal itself has permission to "snoop" on Bluetooth.
Open System Settings (or System Preferences).
Go to `Privacy & Security > Bluetooth.`

#### Getting Started
```shell
source .venv/bin/activate
pip install asyncio bleak rich
python3 bluesnoop.py
```