import serial
import time
import sys


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


def depower(pwr_relay_device):
    ser = init_pwr(pwr_relay_device)
    pwr_off(ser)


def pwr_up(pwr_relay_device):
    ser = init_pwr(pwr_relay_device)
    pwr_on(ser)


pwr_relay_device = "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0"

pwr_relay_port = "usb-1a86_USB_Serial-if00-port0"
pwr_relay_base = "/dev/serial/by-id/"

if __name__ == "__main__":
    we_are = sys.argv.pop(0)
    inputargs = sys.argv

    if len(inputargs) != 2:
        print(we_are, "error: should be two arguments, port and command")
        sys.exit()

    desired = inputargs[0]
    pwr_relay_port = inputargs[1]

    if not (desired == "on" or desired == "off"):
        print(we_are, "error:received command:", desired, " should be on  or off")
        sys.exit()

    pwr_relay_device = pwr_relay_base + pwr_relay_port

    if desired == "on":
        pwr_up(pwr_relay_device)
    else:
        if desired == "off":
            depower(pwr_relay_device)
