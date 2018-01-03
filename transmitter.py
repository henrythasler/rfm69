#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OOK-Decoder"""

import time
from time import sleep
import pigpio as gpio
from lib.rfm69 import Rfm69
import numpy as np

RESET = 24
DATA = 25

micros = lambda: int(round(time.time() * 1000 * 1000))


RECEIVED_SIGNAL = [[], []]  #[[time of reading], [signal reading]]
startticks = 0

def cbf(gpio, level, tick):
    global startticks
    if startticks == 0:
        startticks = tick
    RECEIVED_SIGNAL[0].append((tick-startticks)/1000)
    RECEIVED_SIGNAL[1].append(level)
#    print((tick-startticks)/1000, level)


def main():
    """ main function """
    
    pi = gpio.pi()
    pi.set_mode(RESET, gpio.OUTPUT) 
    pi.set_mode(DATA, gpio.OUTPUT)
    pi.write(DATA, 0)
    pi.write(RESET, 1)
#    time.sleep(.001)
    pi.write(RESET, 0)
    time.sleep(.005)
    
    data = []
    
    with Rfm69(channel=0, baudrate=32000, debug_level=3) as rf:
        rx_data = rf.read_register(0x5A)
        print ''.join('0x{:02x} '.format(x) for x in [rx_data])

        rf.write_register(0x01, 0b00000100)     # OpMode: STDBY
        
        rf.write_address(0x03, [0x03, 0xE8])    # Bitrate: 1000 = 32kb/s
        
#        rf.write_address(0x07, [0x6C, 0x7A, 0xE1]) # Frf: Carrier Frequency 434MHz
        rf.write_address(0x07, [0xD9, 0x14, 0x00])      # Carrier Frequency 868.25MHz
        
        
        rf.write_register(0x1b, 0b01000000)     # OokPeak: peak

#        rf.write_register(0x1b, 0b00000000)     # OokPeak: fixed
#        rf.write_register(0x1d, 70)     # OokFix: 70db


        # rfm69_write_pa_level((1 << 7) | (0x10));
#        rf.write_register(0x18, 0b00000001)     # Lna: 50 Ohm, highest gain
#        rf.write_register(0x19, 0b01000000)     # RxBw: 4% DCC, BW=250kHz

        rf.write_register(0x19, 0b01001001)     # RxBw: 
#        rf.write_register(0x29, 70)             # RssiThreshold: 17.5 dBm

    
        # Read
#        rf.write_register(0x02, 0b01101000)     # DataModul: OOK, continuous w/o bit sync
#        rf.write_register(0x01, 0b10010000)     # OpMode: SequencerOff, Receiver Mode

        # Transmit
        rf.write_register(0x02, 0b01101000)     # DataModul: OOK, continuous w/o bit sync
        rf.write_register(0x01, 0b00001100)     # OpMode: SequencerOff, Receiver Mode

        while (rf.read_register(0x27) & 0x80) == 0:
            print "waiting..."
        print "done"
 
  
        pi.write(DATA, 1)
        start = micros()
        while (micros() - start) < 2000000:
          pi.write(DATA, 1)
          start2 = micros()
          while (micros() - start2) < 1000:
            pass
          pi.write(DATA, 0)
          start2 = micros()
          while (micros() - start2) < 1000:
            pass
          
        pi.write(DATA, 0)


        """
        print '**Started recording**'
        cb1 = pi.callback(DATA, gpio.EITHER_EDGE, cbf)    
        sleep(10)
        cb1.cancel()
        print '**Ended recording**'
        """

        """
        start = micros()
        y = np.empty(0, dtype=np.uint8)
        x = np.empty(0, dtype=np.uint64)
        while (micros() - start) < 10000000:
#            time.sleep(.01)
            x = np.append(x, micros()-start)
#            y = np.append(y, rf.read_register(0x24))
            y = np.append(y, pi.read(DATA))
        """    
        
        np.savez("data", x=RECEIVED_SIGNAL[0], y=RECEIVED_SIGNAL[1])
 #       time.sleep(.1)

    pi.write(RESET, 1)
    pi.write(RESET, 0)
#    time.sleep(.005)

    pi.stop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pi = gpio.pi()
        pi.write(DATA, 0)
        pi.stop()
