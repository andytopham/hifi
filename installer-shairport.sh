#!/bin/bash
echo "** shairport-sync installer **"
echo 'This will take a long time to run - time to grab a coffee (or even dinner).'
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
echo "apt-get installs"
apt-get update
# apt-get -y upgrade
echo "Installing shairport-sync"
# as described in https://github.com/mikebrady/shairport-sync
apt-get -y install build-essential git
apt-get -y install autoconf automake libtool libdaemon-dev libasound2-dev libpopt-dev libconfig-dev
apt-get -y install avahi-daemon libavahi-client-dev
apt-get -y install libssl-dev
apt-get -y install libsoxr-dev
git clone https://github.com/mikebrady/shairport-sync.git
cd shairport-sync
./configure --sysconfdir=/etc --with-alsa --with-avahi --with-ssl=openssl --with-metadata --with-soxr --with-systemd
make
getent group shairport-sync &>/dev/null || sudo groupadd -r shairport-sync >/dev/null
getent passwd shairport-sync &> /dev/null || sudo useradd -r -M -g shairport-sync -s /usr/bin/nologin -G audio shairport-sync >/dev/null
sudo make install
sudo systemctl enable shairport-sync
echo "Installing shairport-sync metadata reader"
# as described in https://github.com/mikebrady/shairport-sync-metadata-reader
git clone https://github.com/mikebrady/shairport-sync-metadata-reader.git
cd shairport-sync-metadata-reader
autoreconf -i -f
./configure
make
sudo make install
echo "Make sure to enable metadata in shairport-sync config file."
echo "Run md-reader by: shairport-sync-metadata-reader < /tmp/shairport-sync-metadata"
