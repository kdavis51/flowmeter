#!/usr/bin/env python

import RPi.GPIO as GPIO
import smtplib, time, sys, os

spigotpin = 11
showerpin = 13
faucetpin = 15
buttonpin = 40

GPIO.setwarnings(false)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(spigotpin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(showerpin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(faucetpin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(buttonpin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

global countspigot,countfaucet,countshower
countspigot = 0
countfaucet = 0
countshower = 0

def countspigotPulse(channel):
   global countspigot
   countspigot= countspigot+1   
   #print "Spigot Pulse: " + str(countspigot)

def countfaucetPulse(channel):
   global countfaucet
   countfaucet= countfaucet+1
   #print "Faucet Pulse: " + str(countfaucet)

def countshowerPulse(channel):
   global countshower
   countshower= countshower+1
   #print "Shower Pulse: " + str(countshower)

def monthlyreset(channel):
   sendemail()

   global spigotflow,faucetflow,showerflow,countshower,countfaucet,countspigot
       
   spigotflow = 0
   faucetflow = 0
   showerflow = 0
   countspigot = 0
   countfaucet = 0
   countspigot = 0
   

cost = "0.00631"

def money(x):
    cost = "0.00631"
    costs = x * float(cost)
    costs = round(costs, 3)
    return "$" + str(costs)

def annual(x):
    ann = x * 365
    ann = round(ann,2)
    return str(ann)


def sendemail():
   os.system('clear')
   print "\n\n SENDING EMAIL...... \n\n"
   
   total = 0
   shower = 0
   faucet = 0
   spigot = 0
   
   total =  spigotflow + faucetflow + showerflow
   
   shower = showerflow
   faucet = faucetflow
   spigot = spigotflow
          
   date = time.strftime("%m/%d/%Y")

   smtpUser = 'poettec2018@gmail.com'
   smtpPass = 'XXXXXXX'

   toAdd = 'td662th@gmail.com'
 
   fromAdd = smtpUser

   subject = "Water Usage"
   header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
   body = "Water use for " + str(date) + ":\nTotal gallons of water used today: " + str(total) + "\n\nIn shower: " + str(shower) + " gallons\n\n" + "From faucet: " + str(faucet) + " gallons\n\nFrom spigot: " + str(spigot) + " gallons\n\nAverage annual water usage: " + annual(total) + " gallons\n\nWater cost for " + str(date) + ":\nTotal cost of gallons today: " + str(money(total)) + "\nFrom shower: " + str(money(shower)) + "\nFrom faucet: " + money(faucet) + "\nFrom spigot: " + money(spigot) + "\nAverage annnual water cost: $" + str(round((int(total) * float(cost) * 365), 2))


   print header + '\n' + body


   s = smtplib.SMTP('smtp.gmail.com',587)
   
   s.ehlo()
   s.starttls()
   s.ehlo()

   s.login(smtpUser, smtpPass)
   s.sendmail(fromAdd, toAdd, header + '\n\n' + body)

   s.quit()
   print ("Finishing sending email, sleeping 10 secs...")
   time.sleep(10)
   os.system('clear')

GPIO.add_event_detect(spigotpin, GPIO.FALLING, callback=countspigotPulse)
GPIO.add_event_detect(faucetpin, GPIO.FALLING, callback=countfaucetPulse)
GPIO.add_event_detect(showerpin, GPIO.FALLING, callback=countshowerPulse)
GPIO.add_event_detect(buttonpin, GPIO.RISING, callback=monthlyreset, bouncetime = 600)

print "\n\nReady to meter.... \n\n"

time.sleep(1)

seconds = 0

spigotflow = 0
faucetflow = 0
showerflow = 0
thirtysecs = 0

while True:
    try:
        time.sleep(1) # sleep 1 second
        seconds = seconds + 1
        thirtysecs = thirtysecs + 1

        # 1 pulse = 2.25 milliliters
        # 1 pulse = 0.00225 liters
        # 1 pulse = 0.00059439 gallons
        # 450 pulses = 1 liter        
        # 1701 pulses = 1 gallon
        
        spigotflow = (countspigot * 0.00059439)
        faucetflow = (countfaucet * 0.00059439)
        showerflow = (countshower * 0.00059439)

        print time.strftime("%m/%d/%Y %H:%M:%S")
        
        print "SPIGOT Gallons consumed: " + str(spigotflow)
        print "FAUCET Gallons consumed: " + str(faucetflow)
        print "SHOWER Gallons sonsumed: " + str(showerflow) + "\n\n\n\n"

        # Sends an email every thirty seconds
        if thirtysecs == 30:
           sendemail()
           thirtysecs = 0
           
        # Sends a monthly email and reset flow meter counters
        if seconds == 262800:
            monthlyreset("")
            seconds = 0                 
        
    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        GPIO.cleanup()
        sys.exit()
