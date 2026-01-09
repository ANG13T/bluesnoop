<p align="center">
  <img align="center" alt="DroneXtract logo" width="600" src="https://github.com/ANG13T/bluesnoop/blob/main/assets/asset_0.png">
</p>

# bluesnoop
A simple Bluetooth Low Energy (BLE) sniffer using Python and the Bleak library

## Preview

<img alt="bluesnoop preview" width="600" src="https://github.com/ANG13T/bluesnoop/blob/main/assets/asset_0.png">

#### Grant Bluetooth Permissions
Since you are using iTerm2, you need to ensure the terminal itself has permission to "snoop" on Bluetooth.
Open System Settings (or System Preferences).
Go to `Privacy & Security > Bluetooth.`

#### Getting Started
```shell
source .venv/bin/activate``
pip install asyncio bleak rich manuf bluetooth-numbers geocoder
python3 bluesnoop.py
```

```
An Organizationally Unique Identifier (OUI) is a 24-bit (three-byte) number, managed by the IEEE, that uniquely identifies a manufacturer or organization for network devices, forming the first half of a device's MAC address to ensure global uniqueness 
```

The uuid.UUID class in Python strictly validates strings against the RFC 4122 standard. Specifically, it looks for a "version" digit at a specific position in the string.

Why it's failing
In a standard UUID, the first digit of the third group (e.g., xxxx-xxxx-**N**xxx-xxxx) must be a number from 1 to 5 (representing the version).

Looking at your data:

D5D93B6E-C324-**F**D7B... -> The version digit is F.

6ADBBD89-CBFF-**0**FE8... -> The version digit is 0.

Since F and 0 are not valid RFC 4122 versions (1-5), Python throws a ValueError: badly formed hexadecimal UUID string.


Explore more on the following:
`discovered_devices_and_advertisement_data` // https://bleak.readthedocs.io/en/latest/api/scanner.html#bleak.BleakScanner.discovered_devices // 16:20 @ 1/8/26 BW


### Interpreting Bluetooth UUID Numbers 

- Use a public OUI database (like the IEEE OUI list) to map MAC address prefixes to manufacturers.
- You can find the OUI database here: https://standards-oui.ieee.org

## Contributing
bluesnoop is open to any contributions. Please fork the repository and make a pull request with the features or fixes you want to be implemented.

## Upcoming
- 

## Support
If you enjoyed bluesnoop, please consider [becoming a sponsor](https://github.com/sponsors/ANG13T) in order to fund my future projects. 

To check out my other works, visit my [GitHub profile](https://github.com/ANG13T).
