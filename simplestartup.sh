#! /bin/sh
# /etc/init.d/simplestartup.sh

### BEGIN INIT INFO
# Provides:          noip
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
# Description:       A modified script from www.stuffaboutcode.com which will start / stop a program a boot / shutdown.
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting display.py"
    # run application you want to start
    /home/pi/hifi/display.py
    ;;
  stop)
    echo "Stopping display.py"
    # kill application you want to stop
    killall display.py
    ;;
  *)
    echo "Usage: /etc/init.d/simplestartup.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
