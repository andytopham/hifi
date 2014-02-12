#!/usr/bin/python
'''Display the song and time on the Volumio display.'''
import oled
import time
import subprocess
import argparse
import logging
import datetime

ROWS = 4
BLANK = "                    "
row = ["" for x in range(ROWS+1)]
oldrow = ["" for x in range(ROWS+1)]
		
def elapsedtime():
	'''Return the elapsed time through the current song.'''
	try:
		p = subprocess.check_output(["mpc"])
		q = p.splitlines()[1].split()[2].split("/")[0]
		logging.info("Elapsed time "+q)
	except:
		q=""
	return(q)

def elapsedpercentage():
	'''Return the elapsed percentage progress through the current song.'''
	try:
		p = subprocess.check_output(["mpc"])
		q = p.splitlines()[1].split()[3].strip("()%")
		logging.info("Elapsed percentage "+q)
	except:
		q=""
	return(q)
	
def updatedisplay():
	'''Write the 4 strings to the OLED.'''
	for i in range(1,ROWS+1):
		if row[i] != oldrow[i]:
			myOled.writerow(i,row[i])
	for i in range(1,ROWS+1):
		oldrow[i] = row[i]

def displaystart():
	'''The main loop for polling mpc for information and putting onto the OLED.'''
	logging.info("Displaystart")
	for i in range(1,ROWS+1):
		row[i] = ""
		oldrow[i] = ""
	counter=0
#	myOled=oled.oled(ROWS)
	myOled.cleardisplay()
	if ROWS == 4:
		timerow = 4
	else:
		timerow = 2
	row[1] = "HiFi Display v1"+BLANK
	row[2] = "Set for "+str(ROWS)+" rows."+BLANK
	updatedisplay()
	# just in case we still have a 4 row connected but have set ROWS=2
	myOled.writerow(3,BLANK)
	myOled.writerow(4,BLANK)
	time.sleep(3)

	while True:
		p = subprocess.check_output(["mpc", "-f", "%artist%", "current"])
		if p == "":				# its stopped
			logging.info("Stopped: "+time.strftime("%R"))
			if ROWS == 4:
				row[1] = BLANK
				row[2] = BLANK
				row[3] = BLANK
				row[4] = time.strftime("%R")+BLANK
			else:
				row[1] = BLANK
				row[2] = time.strftime("%R")+BLANK
			q = ""
		else:					# something is playing
			q = elapsedtime()
			r = elapsedpercentage()
			logging.info("Artist:",p.splitlines()[0])
			row[1] = p+BLANK
			p = subprocess.check_output(["mpc", "-f", "%title%", "current"])
			logging.info("Song:",p.splitlines()[0])
			row[2] = p+BLANK
			if ROWS == 4:
				if len(p) > 20:
					row[3] = p[20:]+BLANK
				else:
					row[3] = BLANK		
				row[4] = ""
				for i in range(0,int(r),5):		# add a char every 5%
					row[4] += ">"
#				row[4] = q+"     "+r+BLANK
		updatedisplay()
		time.sleep(2)
	
if __name__ == "__main__":
	'''Hifi display main routine. Sets up the logging and constants, before calling displaystart.'''
	parser = argparse.ArgumentParser( description='display.py - the Volumio OLED display driver. \
	Use -v option when debugging.' )
	parser.add_argument("-v", "--verbose", help="increase output - lots more logged in ./log/display.log",
                    action="store_true")
	args = parser.parse_args()
	if args.verbose:
		logging.basicConfig(	filename='log/display.log',
								filemode='w',
								level=logging.DEBUG )
	else:
		logging.basicConfig(	filename='log/display.log',
								filemode='w',
								level=logging.WARNING )
	
#	Default level is warning, level=logging.INFO log lots, level=logging.DEBUG log everything
	logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+". Running display.py as a standalone app")
	logging.warning("Use -v command line option to increase logging.")

	print "Running display.py as a standalone app"
	logging.info("OLED rows="+str(ROWS))
	myOled=oled.oled(ROWS)
	displaystart()
	