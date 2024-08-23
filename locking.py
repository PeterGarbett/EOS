import os
import sys

dir_name = "/var/lock"
file_name = "canon20d.lock"

lock = os.path.join(dir_name, file_name)


def lock_if_available():

    if os.path.exists(lock):
        return False
    else:
        with open(lock, "w") as dlock:
            # create the file 'lock' and put the process PID inside
            pid = str(os.getpid())
            dlock.write(pid)
            dlock.close()
            return True


def release_lock():

    if os.path.exists(lock):
        os.remove(lock)


if __name__ == "__main__":

    locked = lock_if_available()
    print(locked)
    locked = lock_if_available()
    print(locked)
    release_lock()
    locked = lock_if_available()
    print(locked)
