"""

Take and save photos from a Canon EOS20D

"""

import os
import sys
import subprocess
import logging
import locale
import gphoto2 as gp
import serial
import time
import camera_pwr
import shutil

sys.path.insert(0, "/home/embed/intrusion")
import filenames
import locking
import EOS_find
import transfer

ATTEMPTS = 5
TIMEOUT = 11
pwr_relay = True
pwr_relay_device = "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0"
pwrup_time = 10


def retrieve(camera, file_path, save_here):
    try:
        target = os.path.join(save_here, file_path.name)
        camera_file = camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
        )
        camera_file.save(target)
        return True
    except Exception as err:
        print(err)
        return False


def finish(camera):
    try:
        camera.exit()
    except Exception as err:
        print(err)


def camera_start():
    locale.setlocale(locale.LC_ALL, "")
    logging.basicConfig(
        format="%(levelname)s: %(name)s: %(message)s", level=logging.WARNING
    )
    callback_obj = gp.check_result(gp.use_python_logging())

    camera = gp.Camera()
    camera.init()
    return camera


def take_photo(camera):
    """Take a photo with timeout error reporting"""

    photo = ""

    try:
        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        return file_path  # .folder +"/"+ file_path.name
    except Exception as err:
        print(err)
        return None


def try_hard_to_take_a_photo(camera):
    """Make several attempts , failures are either no camera or random hanging"""
    for i in range(0, ATTEMPTS):
        result = take_photo(camera)
        if result != None:
            return result

    return ""


def take_and_save_photo(camera):
    """Use camera, save the image and remove from the camera"""
    filepath = try_hard_to_take_a_photo(camera)
    return filepath


photolist = []


def burst(camera, n, save_here):
    """Take N shots then move them"""

    image_names = []

    for i in range(0, n):
        file = take_and_save_photo(camera)
        photolist.append(file)

    for photo in photolist:
        full_path = photo.folder + "/" + photo.name
        retrieve(camera, photo, save_here)
        image_names.append(photo.name)

    return image_names


def get_photos(camera, number, save_here):
    photolist = burst(camera, number, save_here)
    return photolist


def bunch(ser, number, save_here):
    if pwr_relay:
        camera_pwr.pwr_on(ser)

    if not EOS_find.stall_if_camera_not_available(20):
        return []

    camera = None
    photos = []

    try:
        camera = camera_start()
        photos = get_photos(camera, number, save_here)
    except Exception as err:
        print(err)

    finish(camera)

    return photos


def get_images(test, frames, user, hostname, final_dest, remote_path):
    #print(test, frames, user, hostname, final_dest, remote_path)

    locked = locking.lock_if_available()
    if not locked:
        return False

    save_here_first = "/tmp/"
    timestamp = filenames.time_stamped_filename()
    if pwr_relay:
        ser = camera_pwr.init_pwr(pwr_relay_device)

    names = bunch(ser, frames, save_here_first)

    # Modify the filenames so they include timestamps and lb label
    # Copy to somewhere intrusion.py will deal with them i.e. scp etc

    for name in names:
        try:
            if test:
                newname = "testSnapshot_lb4.jpg"
            else:
                newname = timestamp + "_" + name.replace(".JPG", "") + "_lb4.jpg"
                newname = newname.replace("_IMG", "")
            print("Generate", newname)
            os.rename(save_here_first + "/" + name, save_here_first + "/" + newname)
            shutil.move(save_here_first + "/" + newname, final_dest + "/" + newname)
            if test:
                user = "embed"
                hostname = "garbett.cloudns.org"
                remote_path = "/exdrive/Snapshots/Local"

                transfer.send_file(
                    final_dest + "/" + newname, user, hostname, remote_path
                )
        except Exception as err:
            print(err)
            pass

    locking.release_lock()
    return True


if __name__ == "__main__":
    we_are = sys.argv.pop(0)
    inputargs = sys.argv

    if len(inputargs) != 0 and len(inputargs) != 6:
        print(
            we_are,
            "error: calling sequence should be test(bool) frames(int) user hostname local_destination remote_path",
        )
        sys.exit()


    if len(inputargs) == 6:
    #    print(inputargs[0])
        if inputargs[0] == "True":
            test=True
        else:
            test=False

        try:
            frames = int(inputargs[1])
        except Exception as err:
            print(err)
            sys.exit()

        user = inputargs[2]
        hostname = inputargs[3]
        final_dest = inputargs[4]
        remote_path = inputargs[5]

    # Defaults
    if len(inputargs) == 0:
        frames =  8
        test = False
        user = "embed"
        hostname = "garbett.cloudns.org"
        final_dest = "/exdrive/Snapshots/Local"
        remote_path = "/exdrive/Snapshots/Local"

    #print(test, frames, user, hostname, final_dest, remote_path)
    get_images(test, frames, user, hostname, final_dest, remote_path)
