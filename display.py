#!/usr/bin/python
''' 
  Application to display the song and time on the radio display.
  Cut out the debug statements by invoking with python -O display.py (for optimisations)
'''
import oled
import time
import subprocess
		
print "Starting raspyfi display"
counter=0
myOled=oled.oled()
myOled.cleardisplay()
myOled.writerow(1,"Radio Display    ")
#myOled.radiofirstrow()
#song=myOled.raspyfisong()

while True:
	p = subprocess.check_output(["mpc", "-f", "%artist%", "current"])
	if p == "":
		if __debug__: print "Stopped: "+time.strftime("%R")
		myOled.writerow(2,time.strftime("%R")+"             ")
		myOled.writerow(1,p+"                ")
	else:
		if __debug__: print "Artist:",p.splitlines()[0],
		myOled.writerow(1,p+"                ")
		p = subprocess.check_output(["mpc", "-f", "%title%", "current"])
		if __debug__: print "Song:",p.splitlines()[0]
		myOled.writerow(2,p+"                ")
	time.sleep(2)
	
