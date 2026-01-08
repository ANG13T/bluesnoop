# Research

Bleak API Lib Documentation:
https://bleak.readthedocs.io/en/latest/api/index.html

==[`BleakScanner`]============================================================
`<class 'bleak.backends.device.BLEDevice'>`
bleak.backends.device.BLEDevice(address: str, name: str | None, details: Any, **kwargs: Any)

`source`
A simple wrapper class representing a BLE server detected during scanning.

`address`
The Bluetooth address of the device on this machine (UUID on macOS).

`details`
The OS native details required for connecting to the device.

`name`
The operating system name of the device (not necessarily the local name from the advertising data), suitable for display to the user.
=============================================================================