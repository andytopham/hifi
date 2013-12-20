#!/usr/bin/python
''' 
  Application to display the song and time on the radio display.
  
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
#	print "Artist:",p
	if p == "":
	#	p="Stopped"
		myOled.writerow(2,time.strftime("%R")+"             ")
		myOled.writerow(1,p+"                ")
	else:
		myOled.writerow(1,p+"                ")
		p = subprocess.check_output(["mpc", "-f", "%title%", "current"])
#		print "Song:",p
		myOled.writerow(2,p+"                ")
	time.sleep(2)
	
