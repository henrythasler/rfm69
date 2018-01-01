#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OOK-Decoder"""

import time
from lib.rfm69 import Rfm69

def main():
    """ main function """
    with Rfm69() as rf:
        rf.open(0, 32000)
        rx_data = rf.read_register(0x5A)
        print ''.join('0x{:02x} '.format(x) for x in rx_data)

        rf.write_register(0x01, 0b00010000)
        time.sleep(5)

if __name__ == "__main__":
    main()
