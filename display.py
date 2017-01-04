#!/usr/bin/python
'''Display the song and time on the Volumio display.'''
import oled
import time, subprocess, datetime, argparse, logging

ROWS = 2
BLANK = "                    "
LOGFILE="/home/volumio/master/hifi/log/display.log"

row = ["" for x in range(ROWS+1)]
oldrow = ["" for x in range(ROWS+1)]
			
def updatedisplay():
	'''Write the 4 strings to the OLED.'''
	try:
		for i in range(1,ROWS+1):
			if row[i] != oldrow[i]:
				myOled.writerow(i,row[i])
		for i in range(1,ROWS+1):
			oldrow[i] = row[i]
	except:
		logging.warning("failed to update display")

def mpc_status():
	'''Ask mpc what is playing.'''
	p = subprocess.check_output(["mpc"])
	if '[playing]' in p:
		playing = True
		if 'bbc' in p:
			artist = 'BBC'
			title = p.splitlines()[0]
			volume = '0'
			progress = '0'
		else:
			artist = p.splitlines()[0].split('-')[0].strip()
			title = p.splitlines()[0].split('-')[1].strip()
			volume = p.splitlines()[2].split(':')[1].split('%')[0]
			progress = p.splitlines()[1].split()[3].strip('()%')
	else:			# stopped
		playing = False
		artist = 'Stopped'
		title = 'Stopped'
		volume = p.split(':')[1].split('%')[0]
		progress = 0
	logging.info('Artist:'+artist+' Title:'+title+' Vol:'+str(volume)+' Progress:'+str(progress))
	return(playing, artist, title, volume, progress)

def put_time_on_display():
	'''Just put current time on oled, for when nothing playing.'''
	if ROWS == 4:
		row[1] = BLANK
		row[2] = BLANK
		row[3] = BLANK
		row[4] = time.strftime("%R")+BLANK
	else:
		row[1] = BLANK
		row[2] = time.strftime("%R")+BLANK

def show_progress(p, title):
	'''Put the title overflow + progress bar on the oled.'''
	if ROWS == 4:
		if len(title) > 20:
			row[3] = title[20:]+BLANK
		else:
			row[3] = BLANK		
		row[4] = ""
		for i in range(0,int(p),5):		# add a char every 5%
			row[4] += ">"
		row[4] += "     "

def displaystart():
	'''The main loop for polling mpc for information and putting onto the OLED.'''
	logging.info("displaystart")
	for i in range(1,ROWS+1):
		row[i] = ""
		oldrow[i] = ""
	counter=0
	myOled.cleardisplay()
#	print "cleared display"
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
		try:
			playing, artist, title, volume, progress = mpc_status()
		except:
			logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+" Failed to fetch mpc status")
			put_time_on_display()
			row[1] = "mpc_status err"+BLANK
			updatedisplay()
			time.sleep(5)
			continue
		if playing:
			row[1] = artist+BLANK
			row[2] = title+BLANK
			show_progress(progress, title)
		else:				# stopped
			logging.info("Stopped: "+time.strftime("%R"))
			put_time_on_display()
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
		logging.basicConfig(	filename=LOGFILE,
								filemode='w',
								level=logging.DEBUG )
	else:
		logging.basicConfig(	filename=LOGFILE,
								filemode='w',
								level=logging.WARNING )
	
#	Default level is warning, level=logging.INFO log lots, level=logging.DEBUG log everything
	logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+". Running display.py as a standalone app")
	logging.warning("Use -v command line option to increase logging.")

	print "Running display.py as a standalone app"
	logging.info("OLED rows="+str(ROWS))
	time.sleep(5)			# make sure everything is running first
	myOled=oled.oled(ROWS)
	displaystart()
	