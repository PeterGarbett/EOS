import subprocess
import time

TIMEOUT = 0.2


def find_canon20d():
    """See if gphoto2 can find a camera"""
    try:
        command = ["/usr/bin/gphoto2", "--auto-detect"]
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=TIMEOUT, check=True
        )
        if result.returncode != 0:
            return False

        result = result.stdout
        decompose = result.split(" ")
        return "EOS" in decompose
    except Exception as err:
        return False


def stall_if_camera_not_available(attempts):
    """Stall  for a number of .25 second intervals for the camera to hopefully power up"""
    for tries in range(0, attempts):
        if find_canon20d():
            return True
        time.sleep(0.25)

    return False


if __name__ == "__main__":
    cam = stall_if_camera_not_available(20)
    print(cam)
