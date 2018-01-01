#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OOK-Decoder"""

import rfm69

def main():
    """ main function """
    with Rfm69() as rf:
        rf.open(0, 32000)

if __name__ == "__main__":
    main()
