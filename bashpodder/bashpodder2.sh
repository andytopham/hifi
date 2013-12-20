#!/bin/bash
# By Linc 10/1/2004
# Find the latest script at http://lincgeek.org/bashpodder
# Revision 1.21 12/04/2008 - Many Contributers!
# If you use this and have made improvements or have comments
# drop me an email at linc dot fessenden at gmail dot com
# I'd appreciate it!
 
# Make script crontab friendly:
cd $(dirname $0)
 
# datadir is the directory you want podcasts saved to:
#datadir=/media/internal/Podcasts
datadir=/var/lib/mpd/music/podcasts
 
# create datadir if necessary:
mkdir -p $datadir
 
# Delete any temp file:
rm -f temp.log
 
# just creating this if it doesn't exist so we don't get errors on first run
touch podcast.log
 
# Read the bp.conf file and wget any url not already in the podcast.log file:
while read podcast_conf
        do
        set $podcast_conf
        podcast=$1
        max=${2:-999}
        reverse_list=""
        delete_list=""
        count=0
    echo "Handling: $podcast (max=$max)"
        file=$(xsltproc parse_enclosure.xsl $podcast 2> /dev/null || wget -q $podcast -O - | tr '\r' '\n' | tr \' \" | sed -n 's/.*url="\([^"]*.mp3\)".*/\1/p'|uniq)
        for url in $file
                do
                echo $url >> temp.log
                filename=$(echo "$url" | awk -F'/' {'print $NF'} | awk -F'=' {'print $NF'} | awk -F'?' {'print $1'})
        echo -n "  Episode: $filename: "
                if ! grep "$url" podcast.log > /dev/null
                        then
            echo -n "NEED IT"
                        ## if we plan on keeping this file, then get it
                        ## otherwise, we were just going to delete it anyways...
                        if [ $count -lt $max ]
                                then
                echo -n "-DOWNLOADING"
                                wget -U BashPodder -q -O $datadir/$filename "$url"
                                reverse_list="$filename $reverse_list"
            else
                echo -n "-TOO OLD"
                        fi
        else
            echo -n "Already Downloaded"
                fi
        if [ -f $datadir/$filename ]
            then
                    count=$(($count+1))
                    ## if we are over the max, add it to the delete list
                    if [ $count -ge $max ]
                            then
                echo -n "-Will Delete"
                            delete_list="$filename $delete_list"
                    fi
        fi
        echo ""
                done
        # delete the files that are too old
        if [ ! -z "$delete_list" ]
                then
                set $delete_list
                until [ -z "$1" ]
                        do
                echo "  Removing $1"
                                rm -f $datadir/$1 ## ignore errors
                                shift
                        done
                fi
        # touch the files in reverse order so they will be sorted properly
        if [ ! -z "$reverse_list" ]
                then
                set $reverse_list
                until [ -z "$1" ]
                        do
                                ## stupid, but timestamps are too close unless you pause some
                echo "  Touching $1"
                                touch $datadir/$1 && sleep 1
                                shift
                        done
                fi
        done < bp.conf
# Move dynamically created log file to permanent log file:
cat podcast.log >> temp.log
sort temp.log | uniq > podcast.log
rm temp.log