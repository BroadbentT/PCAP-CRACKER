#!/bin/sh

# -------------------------------------------------------------------------------------
#   A SIMPLE BASH UTILITY FILE TO CRACK ENCRYPTED .PCAP FILES CAPTURED BY WIRESHARK
#
#                 BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
#
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
#                    GRAB THE 1ST COMMAND LINE ARGUMENT (.PCAP FILE) 
# -------------------------------------------------------------------------------------

INFILE=$1

# -------------------------------------------------------------------------------------
#                          CONDUCT SOME ROUTINE AND SIMPLE TESTS.
# -------------------------------------------------------------------------------------

if [ $USER != "root" ]
	then echo "Please run this bash script as root..."
	exit 1
else
	echo "\nPCAP-CRACKER - SSID AND WEP KEY CRACKER FOR IEEE (802.11) RADIO .PCAP FILES"
	echo "\n          BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)\n\n\n"
fi

if [ $# -eq 0 ]
	then echo "Use the command sh pcap-cracker.sh wiresharkFile.pcap\n"
	exit 1
else 
	test $INFILE 		
fi

ReturnValue=$?

if [ $ReturnValue != "0" ]
	then exit 1
else 
	echo "Checking associated dependencies are available..."
	type pcapfix > /dev/null
fi

# -------------------------------------------------------------------------------------
#             CHECK ALL REQUIRED DEPENDENCIES ARE INSTALLED ON THE SYSTEM.
# -------------------------------------------------------------------------------------

ReturnValue=$?

if [ $ReturnValue != "0" ]
	then echo "Installing...\n"
	apt-get install pcapfix
	exit 0
else 
	type airmon-ng > /dev/null
fi

ReturnValue=$?

if [ $ReturnValue != "0" ]
	then echo "Installing...\n"
	git clone https://github.com/aircrack-ng/aircrack-ng
	cd aircrack-ng
	autoreconf -i
	./configure --with-experimental
	make
	make install
	cd ..
	exit 0
else 
	type tshark > /dev/null
fi

ReturnValue=$?

if [ $ReturnValue != "0" ]
	then echo "Installing...\n"
	add-apt-repository ppa:dreibh/ppa
	apt-get update
	apt-get install wireshark 
	apt-get install tshark
	exit 0
else 
	echo "All required dependencies are installed..."
fi

# -------------------------------------------------------------------------------------
#     SOMETIMES CAPTURED .PCAP FILES GET CUT OFF OR ARE CORRUPTED IN OTHER WAYS
# -------------------------------------------------------------------------------------

echo "\nOK, I am just going to check your .pcap file for errors..."
pcapfix -d $INFILE -o Fixerror.pcap > /dev/null

test Fixerror.pcap
ReturnValue=$?

if [ $ReturnValue != "0" ]
	then mv $INFILE Oldpcapfile.pcap
	mv Fixerror.pcap $INFILE
	echo "Some errors have been fixed... Your orginal .pcap file is now called Oldpcapfile.pcap.\n"
	exit 0
else 
	echo "Great!!\n"
fi

# -------------------------------------------------------------------------------------
#                       NEXT EXTRACT THE SSID FROM THE .PCAP FILE
# -------------------------------------------------------------------------------------

echo "Now I am going to grab the SSID from the .pcap file..."
SSID=$(tcpdump -ennr $INFILE '(type mgt subtype beacon)' | awk '{print $13}' | sed "s/[()]//g;s/......//" | sort | uniq)
SSID="00:$SSID"
echo $SSID > SSID.txt
echo "Fab!!\n"

# -------------------------------------------------------------------------------------
#           NOW LETS EXTRACT THE WEP KEY FROM THE .PCAP FILE USING THE SSID
# -------------------------------------------------------------------------------------

echo "Lets now grab the WEP KEY from the .pcap file..."
aircrack-ng -b $SSID $INFILE > Key.txt 
grep -o '![^"]*' Key.txt > Key2.txt
cat Key2.txt | sed 's/[^a-z  A-Z 0-1 :]//g' > Key3.txt
cat Key3.txt | tr -d " \t\n\r" > WepKey.txt
rm Key.txt
rm Key2.txt
rm Key3.txt

# -------------------------------------------------------------------------------------
#           USING THE WEP KEY CREATE A CRACKED VERSION OF THE .PCAP FILE
# -------------------------------------------------------------------------------------

WEP=`cat WepKey.txt`
airdecap-ng -w $WEP $INFILE > /dev/null
INFILE=${INFILE%?}
INFILE=${INFILE%?}
INFILE=${INFILE%?}
INFILE=${INFILE%?}
INFILE=${INFILE%?}
INFILE="${INFILE}-dec.pcap"
NEWFILE="Cracked.pcap"
mv $INFILE $NEWFILE
RED='\033[0;31m'
NC='\033[0m'
echo "Super!!\n\n${RED}A cracked version of your .pcap file is now available for use with Wireshark...${NC}"

# -------------------------------------------------------------------------------------
#                  NOW CONDUCT SOME RECONISSANCE ON THE CRACKED FILE
# -------------------------------------------------------------------------------------

echo "\nI will try and export some objects for you, they might contain something of interest!!"
sleep 5
tshark -nr $NEWFILE --export-objects smb,Smbfolder
tshark -nr $NEWFILE --export-objects http,Httpfolder

