#!/usr/bin/env python3
from tkinter import *
import tkinter.messagebox
import time
import os

import subprocess
from subprocess import Popen, PIPE
import base64




def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label2 = Label(frame1, image=frame , bg="black")
    label2.place(x=0, y=0)

    root.after(150, update, ind)

def decrypter():
    dir1 = "important"
    inputvariable = entry.get()
    print(inputvariable)

    subprocess.run(['gpg --pinentry-mode=loopback --passphrase ' + inputvariable + ' --output /' + dir1 + '.tar.gz --decrypt /' + dir1 + '.tar.gz.gpg'], shell=True)
    if os.path.isfile('/' + dir1 + '.tar.gz'):
        subprocess.run(['cd / ; tar xzf ' + dir1 + '.tar.gz'], shell=True)

        if os.path.isdir('/' + dir1):
            tkinter.messagebox.showinfo("Success!!!", "Files Decrypted")
            subprocess.run(['rm /' + dir1 + '.tar.gz.gpg'], shell=True)
            subprocess.run(['rm /' + dir1 + '.tar.gz'], shell=True)

    else:
        tkinter.messagebox.showinfo("Warning!!!", "File Not Decrypted")



root = Tk()

frameCnt = 20
frames = [PhotoImage(file='/media/sf_sharekali/final.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]


frame1 = Frame(root, height=1000, width=800, bg='black'                                                '')
frame1.pack()



entry = Entry(root, text="INPUT CODE",bd=5,fg="black",bg="white",width=40)
entry.place(x=270,y=600,height=30)

button = Button(root, text="VALIDATE CODE", padx=10,pady=10,fg="black",bg="red", command=decrypter)
button.place(x=340,y=550)

update(0)
root.mainloop()