import smbus
import math
import time

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


#reads analog input from the address/port specified
#Returns the digital value (0-1023)

def readAnalogInputPort (i2cPort,  i2cAddress,  adcport):
  
  if (adcport<1) or (adcport>4):
    print ("Port needs to be >0 and <4")
    return -1
  
  
  #Init i2c bus 
  bus = smbus.SMBus(i2cPort) 
  
  #read the lowbyte and hibyte to the address/port of the i2c address
  digitalRaw = bus.read_i2c_block_data (i2cAddress, 0)
  
  #We get 32 bytes back and the first port low byte starts at index 1
  lowbyteIndex=(adcport-1) * 2 +1

  #Get the lowbyte and hibyte for the requested port
  lowbyte= (digitalRaw[lowbyteIndex])
  hibyte= (digitalRaw[lowbyteIndex+1])

  #return the calculated value
  return lowbyte + 255*hibyte
  
#reads analog input from the address/port specified
#Returns the digital value (0-1023)
def readAnalogInputSimple (addressNPort):
  return readAnalogInputPort (addressNPort[0], addressNPort[1], addressNPort[2])
  

#sets analog out to the port specified 
def writeAnalogOutputPort( i2cPort,  i2cAddress,  dacport, value):

  if (dacport<1) or (dacport>4):
    print ("Port needs to be >0 and <4")
    return -1
  
  #Numbering starts with 0 for the smbus.SMBus
  dacport = dacport -1
  
  if value<0 or value>1023:
    print ("setAnalogOut: Value must be between 0 and 1023")
    return -1
  
  #Init i2c bus 
  bus = smbus.SMBus(i2cPort) 
  
  #Calculate high byte and low byte
  hibyte = (value >> 8) & 0x0F
  lowbyte = value & 0xFF
  
  #write the lowbyte and hibyte to the address/port of the i2c address
  bus.write_i2c_block_data (i2cAddress, dacport, [lowbyte, hibyte])
  
  #I found out that if we don't wait after setting analog output, if
  #we read it immediately afterwards (e.g. via ADC the values are screwed.
  time.sleep(0.1)
  return 0
  
#sets analog out to the address/port array specified
def writeAnalogOutputSimple (addressNPort, value):
  return writeAnalogOutputPort (addressNPort[0],addressNPort[1], addressNPort[2], value)




#reads the digital input port and outputs a byte representing the 
#individual input pins
def readDigitalInput ( i2cPort,  i2cAddress):
  bus = smbus.SMBus (i2cPort)
  return bus.read_byte(i2cAddress)
   
#Reads the state of a specific port on the i2c address
#returns 1 if state is HIGH otherwise 0 for LOW
def readDigitalInputPort (i2cPort, i2cAddress, port):
  
  if (port<1) or (port>8):
    print ("Port needs to be >0 and <8")
    return -1
  
  #Reading the input
  iState = readDigitalInput (i2cPort, i2cAddress)

  # We need the bit position of the port. We do this by raising 2 to the power of port-1
  #the result needs to be an integer hence the casting
  port = int(math.pow(2, port-1))

  #If port bit AND the (inverted) read bit are 1 the input is active
  if (port  & ~iState) == port:
    return 1
  
  return 0


#Reads the state of a specifc port on a i2c address/port
#port and address are passed the the function as an array [i2cport, address, port]
def readDigitalInputSimple (addressNPort):
  return readDigitalInputPort (addressNPort[0],addressNPort[1], addressNPort[2])



#Function to read the current state of the digital outputs
#This is the same as reading the digital inputs hence the 
#small cheat (?) 
def readDigitalOutput ( i2cPort,  i2cAddress):
  return readDigitalInput (i2cPort, i2cAddress)

#write the digital outputs
#input is a byte with the bits representing the output ports
#0xFF means no active output port, 0x00 means all active etc.
def writeDigitalOutput (i2cPort, i2cAddress, value):
  
  if (value<0) or (value>255):
    print ("Value needs to be >=0 and <=255")
    return -1
    
  bus = smbus.SMBus (i2cPort)
     
  bus.write_byte(i2cAddress, value)
  return 0

#Writes to digital port
#port and address are passed the the function as an array [i2cport, address, port]
def writeDigitalOutputSimple (addressNPort, value):
  return writeDigitalOutputPort (addressNPort[0],addressNPort[1], addressNPort[2], value)

 
#Set an individual output port
#0 is low and any other value is high
def writeDigitalOutputPort (i2cPort, i2cAddress, port, value):
  if (port<1) or (port>8):
    print ("Port needs to be >0 and <8")
    return -1
   
  #We need the bit position of the port. We do this by raising 2 to the power of port-1
  #the result needs to be an integer hence the casting
  port = int(math.pow(2, port-1))
  
  #reading the current state of the output
  #we wound't want to overwrite the ports that don't interest us... wouldn't we?
  iState = readDigitalInput(i2cPort, i2cAddress)

  if (value==0):
    #if the port should be low then AND the current state witht he port bits
    #if a bit is LOW it'll stay LOW, if it's HIGH it'll stay HIGH
    #unless it is the bit the port wants to be HIGH... then it'll be HIGH
    iState = iState | port 
  else:
    #Reverse if we want to stay HIGH and LOW but want to set HIGH for the port bits
    #Bitwise operations... fun all around!
    iState = iState & ~port
    
  return writeDigitalOutput(i2cPort, i2cAddress, iState)
  

 