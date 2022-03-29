#https://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/

import spidev
import time
import os

spi = spidev.SpiDev()
spi.open(0,0)


def read_channel(channel):
    adc = spi.xfer2([1,(8+channel)<<4, 0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data
