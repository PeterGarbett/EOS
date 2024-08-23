#!/bin/bash 
#

/home/embed/EOS/pwr_on.sh

#Allow time to power up
sleep 5

# Use example routine to clear down camera

/home/embed/EOS/bin/python3 /home/embed/EOS/lib/python3.11/site-packages/gphoto2/examples/clear-space.py  99


