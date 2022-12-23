#!/usr/bin/env python3
from datetime import datetime
from pynput import keyboard
import mac_say
import os
import subprocess
import threading
import time
from subprocess import call


HERE = os.path.dirname(__file__)
HOOKSCRIPT = os.path.join(HERE, "hook.py")
VOLUME = 40


class BorkException(Exception):
    """Urgh!"""


def run(cmd, ignore_errors=False):
    r = subprocess.call(cmd, shell=True)
    if not r == 0 and not ignore_errors:
        raise BorkException()


boothing = False


def on_press(key):
    global boothing

    if(key == keyboard.Key.media_volume_up):
        if(boothing):
            return
        boothing = True
        try:
            booth()
        except Exception as e:
            print(e)
        boothing = False


def countdown():
    mac_say.say(["tre, två, ett", "-v", "Alva"])


def booth():
    print('boothing.')

    ts = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    filename = './photos/booth-{}.jpg'.format(ts)

    t = threading.Thread(target=countdown)
    t.start()

    time.sleep(0.7)

    run('killall PTPCamera 2> /dev/null', ignore_errors=True)

    run('gphoto2 --capture-image-and-download --hook-script {hookscript} --filename {filename}'.format(
        hookscript=HOOKSCRIPT, filename=filename
    ))

    run('killall PTPCamera 2> /dev/null', ignore_errors=True)
    #call([f"osascript -e 'set volume output volume {VOLUME}'"], shell=True)

    print('done!')


if __name__ == '__main__':
    #call([f"osascript -e 'set volume output volume {VOLUME}'"], shell=True)
    with keyboard.Listener(
            on_press=on_press) as listener:
        print("Ready")
        listener.join()
