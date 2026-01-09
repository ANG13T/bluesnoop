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


### Topic Understanding

#### What is `OUI`?
OUI stands for Organizationally Unique Identifier which is a 24-bit number // standed for using first 6 hex digits that identifies a unique manufacturer or vendor on a network

#### OUI IEEE Database
This database is a global master registry used to map network devices to their manufacturers maintainted by IEEE. 
[https://standards-oui.ieee.org/](https://standards-oui.ieee.org/)

Sample Entry Logs:
```
OUI/MA-L                                                    Organization                                 
company_id                                                  Organization                                 
08-EA-44   (hex)		Extreme Networks Headquarters
08EA44     (base 16)		Extreme Networks Headquarters
				2121 RDU Center Drive 
				Morrisville  NC  27560
				US

E4-C7-67   (hex)		Intel Corporate
E4C767     (base 16)		Intel Corporate
				Lot 8, Jalan Hi-Tech 2/3  
				Kulim  Kedah  09000
				MY                                                        
```

#### What is Bluetooth UUID?
Within Bluetooth UUID (Universally Unique Identifier) is an ID for every "Service" (like Heart Rate Monitoring) or "Characteristic" (like the actual Heart Rate measurement).

##### Main Types of Bluetooth UUIDs

`16-bit UUIDs`:  short versions reserved for standard, well-known Bluetooth SIG (Special Interest Group). Example: Heart Rate service is always `0x180D`.

`128-bit UUIDs` custom services created by developers. They look like this: `123e4567-e89b-12d3-a456-426614174000`.

##### Bluetooth UUIDs and RFC protocols
RFCs stand for Request for Comments and act like the law books of the Internet. 

Bluetooth adheres to RFCs to comply with Internet regulations.

The most important rules for Bluetooth UUIDs come from `RFC 4122` (recently updated/obsoleted by `RFC 9562`) and the Bluetooth Core Specification.
