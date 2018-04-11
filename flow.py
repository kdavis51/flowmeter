 import os # importing OS module just in-case needed   
import time # Importing Time module  
import RPi.GPIO as gpio # Importing RPIO module as gpio  
  
  
# Initializing GPIO ports  
boardRevision = gpio.RPI_REVISION # Clearing previous gpio port settings  
gpio.setmode(gpio.BCM) # Use real physical gpio port numbering  

gpio.setup(25, gpio.IN, pull_up_down=gpio.PUD_UP) # setting pin 22 as pull up resistor  
  
  
def showerFlow():  
  showerCurrentTime = int(time.time())  
  showerErrorStopTime = showerCurrentTime + 1  
  showerTimingPulse = 0  
  while showerCurrentTime <= showerErrorStopTime:  
       if gpio.input(25) == True:  
            if gpio.input(25) == False:  
                 showerTimingPulse += 1  
            else:  
                 showerCurrentTime = int(time.time())  
       else:  
            showerCurrentTime = int(time.time())  
  
  if showerTimingPulse != 0:  
       showerStartTime = int(time.time())  
       print 'shower start time', showerStartTime  
       waitTimershower = showerStartTime + 2  
       waitTimerCountshower = int(time.time())  
       showerCount = 0  
       print 'shower count', showerCount  
       while (showerCount < 15) and (waitTimerCountshower <= waitTimershower) :  
            if gpio.input(25) == True:  
                 if gpio.input(25) == False:  
                      showerCount += 1  
                      print 'shower count', showerCount  
                      waitTimershower = int(time.time()) + 1  
                 else:  
                      waitTimerCountshower = int(time.time())  
            else:  
                 waitTimerCountshower = int(time.time())  
       showerEndTime = int(time.time())  
       print 'shower end time', showerEndTime  
       if showerCount == 15:  
            showerSecsPerLiters = showerEndTime - showerStartTime  
            showerLitersPerHour = (3600.0 / showerSecsPerLiters) * 30  
            showerGalPerHour = showerLitersPerHour * 0.26417205235815  
            return showerGalPerHour  
       else:  
            showerGalPerHour = 0  
       return showerGalPerHour  
  else:  
       showerGalPerHour = 0  
       return showerGalPerHour  
  
while True:  
  showerGalPerHour = showerFlow()  
  print "shower flow =", showerGalPerHour, "Gal/Hour"  
