#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""RFM69-Class"""

import pigpio as gpio

# global defines
ERROR = 1
INFO = 2
TRACE = 3

class Rfm69(object):
    """RFM69-Class"""
    # pylint: disable=too-many-instance-attributes, C0301, C0103

    def __init__(self, debug_level=0):
        # general variables
        self.debug_level = debug_level

        # RFM69-specific variables
        self.handle = None
        self.pi = gpio.pi()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """clean up stuff"""
        if self.handle:
            self.pi.spi_close(self.handle)
        self.pi.stop()

    def debug(self, message, level=0):
        """Debug output depending on debug level."""
        if self.debug_level >= level:
            print message

    def open(self, channel=0, baudrate=10000000):
        """Open SPI interface"""
        self.handle = self.pi.spi_open(channel, baudrate, 0)    # Flags: CPOL=0 and CPHA=0

    def read_register(self, address):
        """Read register via spi"""
        (count, data) = self.pi.spi_xfer(self.handle, [address, 0x00])
        if count == 2:
            return data[1::]
        return None

    def write_register(self, address, value):
        """Write register via spi"""
        (count, data) = self.pi.spi_xfer(self.handle, [address & 0x80, value])
        return count == 2
