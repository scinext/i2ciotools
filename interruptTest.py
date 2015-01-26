#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import i2ciotools
import sys


I2C_PORT=1
#i2c addresse of the DI module
DI_MODULE_1_ADDR=0x20

#GPIO the INT (Interrupt) Signal of the Horter I2C Repeater is wired to
INT_GPIO=17

DI = [0,0,0,0,0,0,0,0]

# Interrupt handler
def Interrupt(channel): 
    global DI
    print("Interrupt!")
    #The list of for the new values
    DI_new = [0,0,0,0,0,0,0,0]
    
    #read all inputs sequentially
    for i in range (1,8):
      DI_new[i-1]=i2ciotools.readDigitalInputPort(I2C_PORT, DI_MODULE_1_ADDR, i)
    
    #Now check if the new value equals the old value
    #if it does... nothing changes
    for i in range (0,7):
      if (DI[i] != DI_new[i]):
        #If old doesn't match new value... that PIN changed
        print("PIN "+str(i)+" changed")
    #print out a list of the current state of all inputs
    for i in range(0,7):    
      sys.stdout.write(str(DI[i]))
      sys.stdout.write(" ")
    print("")
    print("")
    #Don't forget that step... new=old
    DI=DI_new
      
    
    
    
    
# Setup the GPIO
GPIO.setmode(GPIO.BCM)  
GPIO.setup(INT_GPIO, GPIO.IN)  
# Add Interrupt on GPIO 4 on FALLING edge. 
# Be aware that the bouncetime may need to change in our environment.
GPIO.add_event_detect(INT_GPIO, GPIO.RISING, callback = Interrupt, bouncetime = 200)   
print ("Interrupt handler set... waiting")
print (i2ciotools.readDigitalInput(I2C_PORT, DI_MODULE_1_ADDR))
    
while True:
  print (".")
  time.sleep(100)
        

