#!/bin/sh
echo "** Installing fileset needed for hifi appliance display system. **"
# first, check user is root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
echo "hifi display installer"
echo
echo "apt-get update"
apt-get update
echo
echo "apt-get -y upgrade"
apt-get -y upgrade
echo
echo "apt-get -y install python-pip"
apt-get -y install python-pip
echo
echo "pip install beautifulsoup4"
pip install beautifulsoup4
echo
echo "pip install requests"
pip install requests
echo
echo "pip install python-mpd2"
pip install python-mpd2
echo
echo "pip install logging"
pip install logging
echo
echo "apt-get -y install python-serial"
apt-get -y install python-serial
echo
echo "install feedparser"
pip install feedparser
pip install urllib3
echo
echo "apt-get -y install mpd mpc"	
apt-get -y install mpd mpc	
mkdir log
echo "Starting autostart of display.py"
cp hifistartup.sh /etc/init.d
chmod 755 /etc/init.d/hifistartup.sh
update-rc.d hifistartup.sh defaults
chmod +x display.py
# This next bit only works for Volumio 1
# BBC stream locations can be found at....
# http://www.suppertime.co.uk/blogmywiki/2015/04/updated-list-of-bbc-network-radio-urls/
echo "Copy BBC playlist files"
cp BBCR* /var/lib/mpd/music/WEBRADIO

echo "** ToDo: **"
echo "Disable linux write to serial port by removing AMA refs in /boot/cmdline.txt"
echo "Enable serial port by adding enable_uart=1 to /boot/cmdline.txt"
echo " ********* "
