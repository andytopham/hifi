#!/bin/sh
# get the shairport stuff going
/home/pi/master/hifi/shairport-sync/shairport-sync-metadata-reader/shairport-sync-metadata-reader < /tmp/shairport-sync-metadata | python /home/pi/master/hifi/shairMDdisplay.py -v
