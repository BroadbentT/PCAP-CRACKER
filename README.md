# PCAP CRACKER
## A PYTHON SCRIPT FILE TO DECRYPT ENCRYPTED IEEE (802.11) RADIO PCAP FILES CAPTURED VIA WIRESHARK.

Usage: python pcap-cracker.py monitored.pcapng

| LANGUAGE | FILENAME          | MD5 HASH                         | CONTAINS         |
|--------  |---------          |---------                         | -------          |
| python   | pcap-cracker.py   | 512375beb41e93bc213c3b5fa3afb0e4 |                  |
| zip      | Wiresharkfile.zip | 8e2d9661621cf49a04dc2cb2064161ae | Monitored.pcapng |

A python script file to decrypt encrypted IEEE (802.11) Radio .pcap files captured via Wireshark. 
The script first extracts the Service Set IDentifier (SSID), and uses it to obtain the Wired Equivalent Privacy (WEP) key.
Once the WEP key has been extracted - it then decrypts the .pcap file completly (Cracked.pcap).

__Bonus!! now includes automated username, password and object exporter.__

### CONSOLE DISPLAY
![Screenshot](picture1.png) 
