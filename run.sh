#!/bin/sh
/home/pi/shairport/shairport-sync-metadata-reader/shairport-sync-metadata-reader < /tmp/shairport-sync-metadata | python shairMDdisplay.py -v
