#!/usr/bin/python


# Copyright (c) 2015, Ingo Schubert (dmidb1@gmail.com)
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * The names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# Sample that shows the usage of the Interrupt signal from the Digital Input Module


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
        

