#!/usr/bin/python


#Sample script to show the usage of the i2ciotools.py library together with the Horter I2C modules
#To complete the entire script you need all 4 modules (Digital In and Out, Analog In and Out)
#This script assumes you wired the modules in a way that Digital Output 1 is connected to
#Digital Input 1. Analog Output 1 should be wired to Analog Input 1
#This is all done just to so we can set something and read it to show output and input... clever isn't it?
#If you don't have all modules just look at the source and it becomes pretty clear which parts are of
#interest for your use case.
#The i2ciotools offer a number of ways to address the digital input and output modules
#You can go low level and provide/read the full byte (0x00 to 0xff) or address individual PINs/Ports
#This sample script shows them all! 
#I take it you'll pick the easiest way... whatever that might be in your case.

import i2ciotools
import time

I2C_PORT=1
#i2c addresses
DI_MODULE_1_ADDR=0x20
DO_MODULE_1_ADDR=0x24
AO_MODULE_1_ADDR=0x58
AI_MODULE_1_ADDR=0x18

EXAMPLE_DIGITAL_OUTPUT=[I2C_PORT, DO_MODULE_1_ADDR, 1]
EXAMPLE_DIGITAL_INPUT=[I2C_PORT, DI_MODULE_1_ADDR, 1]

EXAMPLE_ANALOG_OUTPUT=[I2C_PORT, AO_MODULE_1_ADDR, 1]
EXAMPLE_ANALOG_INPUT=[I2C_PORT, AI_MODULE_1_ADDR, 1]


counter = 0

#Digital Output examples

#Blink 5 times
print ("<blink>")

try:
  while (counter<5):
    print (".")
    time.sleep(0.5)
    i2ciotools.writeDigitalOutputSimple(EXAMPLE_DIGITAL_OUTPUT, 1)
    time.sleep(0.5)
    i2ciotools.writeDigitalOutputSimple(EXAMPLE_DIGITAL_OUTPUT, 0)
    counter = counter + 1
except:
  print ("ERROR! The DO module isn't wired or you provided the wrong address")
  
  
quit()

#Check out all the options to read/write digital input/output
#Pick the one you like most. 

try:
  #Set the output PIN/Port 1 to 1 (active)   
  i2ciotools.writeDigitalOutputSimple(EXAMPLE_DIGITAL_OUTPUT, 1)
except:
  print ("ERROR! The DO module isn't where it is supposed to be")

try:
  if (i2ciotools.readDigitalInputSimple(EXAMPLE_DIGITAL_INPUT)==1):
    print ("Input is active")
  else:
    print ("Input is NOT active")
except:
  print ("ERROR! The DI module isn't there. Check the wires and the address")


#OK, enough with the exception catching for each statement. If you have just DI or DO
#the following code block won't execute correctly as the first time a non-existing module
#is used the code will fail and go to the except statement

try: 
  #Set the output PIN/Port 1 to 0 (inactive)
  #Use the slightly different writeDigitalOutputPort to do that...
  i2ciotools.writeDigitalOutputPort(I2C_PORT, DO_MODULE_1_ADDR, 1, 0)

  #Read using the readDigitalInputPort 
  if (i2ciotools.readDigitalInputPort(I2C_PORT, DI_MODULE_1_ADDR,1)==1):
    print ("Input is active")
  else:
    print ("Input is NOT active")

  #Let's go hardcore and send the byte directly (note the negated byte)  
  #Set the output PIN/Port 1 to 1 (active)   
  i2ciotools.writeDigitalOutput(I2C_PORT, DO_MODULE_1_ADDR, 0xFE)

  if (i2ciotools.readDigitalInput(I2C_PORT, DI_MODULE_1_ADDR)==0xFE):
    print ("Input is active")
  else:
    print ("Input is NOT active")
  
  #Set the output PIN/Port 1 to 0 (inactive)
  #Back to the shortest notation...
  i2ciotools.writeDigitalOutputSimple(EXAMPLE_DIGITAL_OUTPUT, 0)

  if (i2ciotools.readDigitalInputSimple(EXAMPLE_DIGITAL_INPUT)==0xfe):
    print ("Input is active")
  else:
    print ("Input is NOT active")
  
except:
  print ("ERROR! DI and DO... you really should check the addresses of these modules and if you wired them correctly")

#Analog Output test

print ("Setting Analog out to 700 (7V)")

try:
  i2ciotools.writeAnalogOutputPort (I2C_PORT, AO_MODULE_1_ADDR,1, 700)
except:
  print ("ERROR! That AO module... is it there?")

#Reading it back in (slightly different input values are thanks to the combination of variations in the DA and AD converters.
try:
  print ("Analog Input Value on Port 1 is: " + str(i2ciotools.readAnalogInputSimple (EXAMPLE_ANALOG_INPUT)))
  print ("Analog Input Value on Port 1 is (again!): "+str(i2ciotools.readAnalogInputPort (1, 0x18,1)))
except:
  print ("ERROR! That AI module... are you sure you wired it up correctly?")


#Set 10 V and reduce by about .5 V every 0.1 second
counter = 1023
print ("Setting 10V... and going towards 0V")
while (counter>0):
  print (".")
  try:
    i2ciotools.writeAnalogOutputSimple (EXAMPLE_ANALOG_OUTPUT, counter)
  except:
    print ("..")
  time.sleep(0.1)
  counter = counter - 50
  

#Setting analog output to 0
try:
  i2ciotools.writeAnalogOutputSimple (EXAMPLE_ANALOG_OUTPUT, 0)
except:
  print ("AO still isn't working...")

