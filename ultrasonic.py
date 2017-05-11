import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
from pymongo import MongoClient
from time import gmtime, strftime
from datetime import datetime


GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIG = 23                                  #Associate pin 23 to TRIG
ECHO = 24                                  #Associate pin 24 to ECHO

client = MongoClient("mongodb://main:mainuser@ds137291.mlab.com:37291/zurkovic_iot")
db = client.zurkovic_iot

print "Distance measurement in progress"

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in

while True:

  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  print "Calibrating..."
  time.sleep(2)                            #Delay of 2 seconds

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                      #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
    pulse_start = time.time()              #Saves the last known time of LOW pulse

  while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
    pulse_end = time.time()                #Saves the last known time of HIGH pulse 

  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            #Round to two decimal points

  date_time = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

  if (distance < 5):
    print("Alarm triggered at " + str(date_time) + "With " + str(distance))

    result = db.triggers.insert_one(
    {
	"date": datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f'),
        "triggered": 1
    })

'''
  if distance > 2 and distance < 400:      #Check whether the distance is within range
    print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
  else:
    print "Out Of Range"                   #display out of range
'''

