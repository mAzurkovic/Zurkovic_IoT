import RPi.GPIO as GPIO                    # Import GPIO library
import time                                # Import time library
from pymongo import MongoClient
from time import gmtime, strftime
from datetime import datetime


GPIO.setmode(GPIO.BCM)                     # Set GPIO pin numbering 

TRIG = 23                                  
ECHO = 24                                  

client = MongoClient("mongodb://main:mainuser@ds137291.mlab.com:37291/zurkovic_iot")
db = client.zurkovic_iot

print "Distance measurement in progress"

GPIO.setup(TRIG,GPIO.OUT)                  
GPIO.setup(ECHO,GPIO.IN)                   

while True:

  GPIO.output(TRIG, False)                 
  print "Reading ..."
  time.sleep(2)                            

  GPIO.output(TRIG, True)                  
  time.sleep(0.00001)                      
  GPIO.output(TRIG, False)                 

  while GPIO.input(ECHO)==0:               
    pulse_start = time.time()              

  while GPIO.input(ECHO)==1:               
    pulse_end = time.time()                 

  pulse_duration = pulse_end - pulse_start 

  distance = pulse_duration * 17150        # Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            # Round to two decimal points

  # Get standard date and time
  date_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

  if (distance < 5):
    print("Alarm triggered at " + str(date_time) + "With " + str(distance))

    # Make mongo schema and save it to datastore @mlab
    result = db.triggers.insert_one(
    {
	"date": date_time,
        "triggered": 1,
	"distance": distance
    })
