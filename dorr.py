#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import os
import sys
import wiringpi
from path import path

continue_reading = True

card_id = ("No cards Yet")

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()
 
# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
 
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
 
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
	global continue_reading
	print("Ctrl+C captured, ending read.")
	continue_reading = False
	GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to Tokilokit's lock / unlock script! (Thanks to Mario Gomez for the original script)")
print("Press Ctrl-C to stop.")

# Unlock as default

wiringpi.pwmWrite(18, 180)

time.sleep(.5)

wiringpi.pwmWrite(18, 0)

os.system("echo 1 > /home/pi/dorr/state")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:


	lock = path("/home/pi/dorr/state").bytes()

	# Scan for cards
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

	# Get the UID of the card
	(status,uid) = MIFAREReader.MFRC522_Anticoll()

	# If we have the UID, continue
	if status == MIFAREReader.MI_OK:

		# Print UID
		card_id = "%x:%x:%x:%x" % (uid[0], uid[1], uid[2], uid[3])
		print("card detected", card_id)


		if ((card_id == "ex:am:pl:e1") | (card_id == "ex:am:pl:e2")):
        
		    if lock == "0\n":
                print("Key detected, unlocking if I need to")
                print("unlocked")
                os.system("echo 1 > /home/pi/dorr/state")
                wiringpi.pwmWrite(18, 200)
            else:
                print("Key detected, locking if I need to")
                print("locked")
                os.system("echo 0 > /home/pi/dorr/state")
                wiringpi.pwmWrite(18, 76)


		time.sleep(.5)

		wiringpi.pwmWrite(18, 0)
