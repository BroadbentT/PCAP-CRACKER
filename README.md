# PCAP-CRACKER

python pcap-cracker.sh wiresharkfile.pcap

A simple python file to decrypt encrypted IEEE (802.11) Radio .pcap files captured via Wireshark.
The script file first extracts the SSID, and then uses it to obtain the WEP key.
Once the wep-key has been extracted - it then decrypts the .pcap file completly.

Bonus!! now includes automated username/password/objects export.

![Screenshot1](Image1.PNG)

![Screenshot2](Image2.PNG)


