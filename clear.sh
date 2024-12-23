#!/bin/bash 
#
#exit
/home/embed/EOS/pwr_on.sh
sleep 5

/home/embed/EOS/bin/python3 /home/embed/EOS/lib/python3.11/site-packages/gphoto2/examples/clear-space.py  99

# Need to delete folders as well. If we don't the camera stops working
# when  folder 999 exists

gphoto2 --delete-all-files --debug --debug-logfile=/home/embed/EOS/delete_log.txt

