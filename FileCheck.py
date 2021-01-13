#! /usr/bin/env python3
import subprocess
from subprocess import Popen, PIPE
import base64
import os.path
from os import path


def checker():
    os.makedirs('/tmp/r00t', exist_ok = True)
    subprocess.run(['mount -t nfs 10.0.2.10:/ /tmp/r00t/'], shell=True)
    if path.exists('/tmp/r00t/lotus') == True:
        print('yes!')
    else:
        print('Nope :(')
    




    subprocess.run(['umount /tmp/r00t'], shell=True)


checker()
