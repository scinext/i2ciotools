# Introduction #

The i2ciotools python library is intended for communicating with the Horter I2C digital/analog input/output modules.

It was developed for usage with the Raspberry Pi but should work on any platform.

It may also work with other I2C digital input/output modules that are PCF8574 based but this hasn't been tested.


# Details #

The library is compatible with Python 2.7 - not Python 3 as that one lacks the smbus library.

Look at the i2ctestbed.py to see examples on how to use the library.

interruptTest.py has a simple interrupt handler that makes use of the INT signal from the digital input module.

Don't know the address of your modules? Try this command line which gives out the addresses you nee to provide to the i2ciotools functions:

i2cdetect -y 1


