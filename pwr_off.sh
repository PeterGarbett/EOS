#!/bin/bash

/home/embed/EOS/bin/python3  usb_pwr_relay.py  off usb-1a86_USB_Serial-if00-port0

rm -f /var/lock/canon20d.lock
