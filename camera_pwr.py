import serial
import time
import sys

pwr_relay_device = "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0"


def init_pwr(pwr_relay_device):
    try:
        ser = serial.Serial(port=pwr_relay_device, baudrate=9600, timeout=0.5)
    except Exception as err:
        print(err)
        return None
    if not ser:
        print("Can't find: ", pwr_relay_device)
        return None

    return ser


def pwr_on(ser):
    on_command = b"\xA0\x01\x01\xA2"

    if not ser:
        return

    try:
        ser.write(on_command)
    except Exception as err:
        print(err)
        return None

    return


def pwr_off(ser):
    if not ser:
        return

    try:
        off_command = b"\xA0\x01\x00\xA1"
        ser.write(off_command)
    except Exception as err:
        print(err)


def depower():

    ser = init_pwr(pwr_relay_device)
    pwr_off(ser)

def pwr_up():

    ser = init_pwr(pwr_relay_device)
    pwr_on(ser)


if __name__ == "__main__":
    depower()
    #sleep(15)
    #pwr_up()
